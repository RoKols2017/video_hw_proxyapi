import os
import logging

from src.video_app.interfaces.flask_app import create_flask_app


logger = logging.getLogger(__name__)


def create_app():
    return create_flask_app()


app = create_app()


if __name__ == "__main__":
    from src.video_app.config.settings import get_settings

    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.DEBUG),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    logger.info("[app.__main__] starting Flask application", extra={"host": host, "port": port})
    app.run(host=host, port=port, debug=False)
