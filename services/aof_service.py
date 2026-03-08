from core.redis import redis_client

class AOFService:

    @staticmethod
    def get_aof_status():
        info = redis_client.info("persistence")
        return {
            "aof_enabled": bool(info.get("aof_enabled")),
            "aof_rewrite_in_progress": bool(info.get("aof_rewrite_in_progress")),
            "aof_last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec"),
            "aof_current_size": info.get("aof_current_size"),
            "aof_base_size": info.get("aof_base_size"),
            "aof_last_bgrewrite_status": info.get("aof_last_bgrewrite_status")
        }

    @staticmethod
    def trigger_aof_rewrite():
        try:
            redis_client.bgrewriteaof()
            return {"message": "AOF rewrite triggered successfully in the background"}
        except Exception as e:
            return {"error": str(e)}