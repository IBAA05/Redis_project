from fastapi import APIRouter, Depends
from services.overdue_producer import OverdueProducer
from services.overdue_consumer import OverdueConsumer
from core.dependencies import admin_only

router = APIRouter(
    prefix="/overdue",
    tags=["⏰ Overdue Borrow Stream"],
)


@router.post(
    "/scan",
    summary="Scan & detect overdue borrows",
    description=(
        "Runs the full overdue pipeline in two steps:\n\n"
        "1. **Producer** — scans all active borrow hashes in Redis, compares each "
        "`due_date` to today, and publishes an event to `overdue_stream` via `XADD` "
        "for every overdue borrow.\n\n"
        "2. **Consumer** — reads those events from `overdue_stream` via `XREADGROUP`, "
        "sets `status = overdue` on each borrow hash (`HSET borrow:{book_id} status overdue`), "
        "and acknowledges the messages with `XACK`.\n\n"
        "The response contains a full breakdown of what was scanned, published, and processed.\n\n"
        "**Auth**: Bearer token required (admin only).\n\n"
        "**Postman tip**: no request body needed — just call POST with your Bearer token."
    ),
    response_description="Summary of the scan + processing result",
    responses={
        200: {
            "description": "Overdue scan completed",
            "content": {
                "application/json": {
                    "example": {
                        "producer": {
                            "scanned": 5,
                            "published": 2,
                            "overdue_book_ids": ["b-001", "b-003"],
                        },
                        "consumer": {
                            "processed": 2,
                            "details": [
                                {
                                    "msg_id": "1741471200000-0",
                                    "book_id": "b-001",
                                    "user_id": "user42",
                                    "due_date": "2026-01-15",
                                    "days_overdue": 52,
                                },
                                {
                                    "msg_id": "1741471200001-0",
                                    "book_id": "b-003",
                                    "user_id": "user07",
                                    "due_date": "2026-02-01",
                                    "days_overdue": 35,
                                },
                            ],
                        },
                    }
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def scan_overdue():
    producer_result = OverdueProducer.scan_and_publish()
    consumer_result = OverdueConsumer.process_overdue_events()
    return {"producer": producer_result, "consumer": consumer_result}


@router.get(
    "/list",
    summary="List all overdue borrows",
    description=(
        "Returns every borrow that has already been **marked as overdue** "
        "(i.e. `status = overdue` in Redis).\n\n"
        "A borrow is marked overdue only after `POST /overdue/scan` has been called — "
        "this endpoint just reads what is already stored in Redis.\n\n"
        "**Auth**: Bearer token required (admin only).\n\n"
        "**Postman tip**: call `POST /overdue/scan` first, then use this endpoint to list results."
    ),
    response_description="List of overdue borrow records",
    responses={
        200: {
            "description": "Overdue borrows",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "book_id": "b-001",
                            "user_id": "user42",
                            "borrow_date": "2026-01-01",
                            "due_date": "2026-01-15",
                            "status": "overdue",
                        }
                    ]
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def list_overdue():
    return OverdueConsumer.list_overdue_borrows()


@router.get(
    "/stream/info",
    summary="Overdue stream metadata",
    description=(
        "Returns the total number of messages currently stored in `overdue_stream`.\n\n"
        "Useful to verify that the producer has published events before triggering the consumer.\n\n"
        "**Auth**: Bearer token required (admin only)."
    ),
    response_description="Stream name and total message count",
    responses={
        200: {
            "description": "Overdue stream metadata",
            "content": {
                "application/json": {
                    "example": {
                        "stream": "overdue_stream",
                        "total_messages": 2,
                    }
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def overdue_stream_info():
    from repositories.stream_repository import StreamRepository, OVERDUE_STREAM
    length = StreamRepository.stream_length(OVERDUE_STREAM)
    return {"stream": OVERDUE_STREAM, "total_messages": length}
