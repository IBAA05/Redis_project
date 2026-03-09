from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from services.stream_service import StreamService
from core.dependencies import admin_only

router = APIRouter(
    prefix="/stream",
    tags=["📡 Activity Event Stream"],
)


@router.get(
    "/info",
    summary="Stream metadata",
    description=(
        "Returns basic metadata about the **audit_stream** Redis Stream: "
        "the stream name and total number of events ever published.\n\n"
        "**Auth**: Bearer token required (admin only)."
    ),
    response_description="Stream name and total event count",
    responses={
        200: {
            "description": "Stream metadata",
            "content": {
                "application/json": {
                    "example": {
                        "stream": "audit_stream",
                        "total_events": 42,
                    }
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def get_stream_info():
    return StreamService.get_stream_info()


@router.get(
    "/events",
    summary="Get latest activity events",
    description=(
        "Reads the latest **N** events from the `audit_stream` Redis Stream "
        "(newest first via `XREVRANGE`).\n\n"
        "Events are published automatically whenever a book is borrowed, returned, "
        "reviewed, or any other major action occurs.\n\n"
        "**Auth**: Bearer token required (admin only).\n\n"
        "**Postman tip**: set `count` as a query parameter, e.g. `?count=20`."
    ),
    response_description="List of activity events, newest first",
    responses={
        200: {
            "description": "Activity events from the stream",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "1741471200000-0",
                            "action": "BOOK_BORROWED",
                            "description": "user42 borrowed Clean Code",
                            "book_id": "b-001",
                            "user_id": "user42",
                            "timestamp": "2026-03-08 22:00:00",
                        }
                    ]
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def get_all_events(
    count: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Maximum number of events to return (1–500)",
    )
):
    return StreamService.get_all_events(count=count)


@router.post(
    "/events/publish",
    summary="Manually publish an event",
    description=(
        "Manually publish a custom event to the `audit_stream`.\n\n"
        "Useful for testing the stream pipeline or injecting administrative notes.\n\n"
        "**Auth**: Bearer token required (admin only).\n\n"
        "**Postman tip**: send a JSON body with `action`, `description`, "
        "and optionally `book_id` / `user_id`."
    ),
    response_description="Redis message ID assigned to the published event",
    responses={
        200: {
            "description": "Event published successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Event published",
                        "redis_id": "1741471200000-0",
                        "action": "MANUAL_NOTE",
                    }
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def publish_event(
    action: str = Query(..., description="Event type, e.g. MANUAL_NOTE, SYSTEM_CHECK"),
    description: str = Query(..., description="Human-readable description of the event"),
    book_id: str = Query(default="", description="(Optional) book ID this event relates to"),
    user_id: str = Query(default="", description="(Optional) user ID this event relates to"),
):
    redis_id = StreamService.publish_event(action, description, book_id, user_id)
    return {"message": "Event published", "redis_id": redis_id, "action": action}


@router.get(
    "/events/{book_id}",
    summary="Get events for a specific book",
    description=(
        "Returns all activity events from the `audit_stream` that are linked to the "
        "given `book_id`, newest first.\n\n"
        "**Auth**: Bearer token required (admin only).\n\n"
        "**Postman tip**: set the path parameter `book_id` and optionally `?count=N`."
    ),
    response_description="Events for the specified book",
    responses={
        200: {
            "description": "Events for this book",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "1741471200000-0",
                            "action": "BOOK_BORROWED",
                            "description": "user42 borrowed Clean Code",
                            "book_id": "b-001",
                            "user_id": "user42",
                            "timestamp": "2026-03-08 22:00:00",
                        }
                    ]
                }
            },
        },
        403: {"description": "Admin access required"},
    },
    dependencies=[Depends(admin_only)],
)
def get_events_by_book(
    book_id: str,
    count: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Maximum number of events to scan (1–500)",
    ),
):
    return StreamService.get_events_by_book(book_id=book_id, count=count)
