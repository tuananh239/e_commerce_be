# ===========================================================================================
# Application
# Dev: anh.vu
# ===========================================================================================

"""
    Khởi tạo ứng dụng và thêm các controller
"""

# ===========================================================================================

from fastapi.middleware.cors import CORSMiddleware

from app.libs.fastapi.app import app, add_router

from app.src.commons.constants.constants import APP_CONST
from app.src.controllers.user_controller import user_controller
from app.src.controllers.decision_controller import decision_controller
from app.src.controllers.petition_controller import petition_controller
from app.src.controllers.commitment_controller import commitment_controller

# ===========================================================================================

# Main class ================================================================================
app.title = APP_CONST.TITLE
app.description = APP_CONST.DESCRIPTION
app.version = APP_CONST.VERSION

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

controllers = [
    decision_controller,
    petition_controller,
    commitment_controller,
    user_controller
]

add_router(
    application=app,
    prefix_path=f"{APP_CONST.CONTEXT_ROOT}{APP_CONST.VERSION}",
    routers=controllers
)

# kafka_controller = KafkaController(
#     consumers=[
#         ocr_coordinator_consumer
#     ]
# )

# schedule_controller = ScheduleController(
#     jobs = [
#         schedule_job
#     ]
# )

# Implement =================================================================================
# @app.on_event("startup")
# async def startup_event():
#     kafka_controller.start_all()
    # schedule_controller.start_all()


# @app.on_event("shutdown")
# async def shutdown_event():
#     kafka_controller.stop_all()
    # schedule_controller.stop_all()

