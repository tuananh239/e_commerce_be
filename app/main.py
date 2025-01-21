# ===========================================================================================
# Main
# Dev: anh.vu
# ===========================================================================================

import sys
import uvicorn
import decouple

# Set relative path
[sys.path.append(i) for i in ['.', '..']]
# Load environment
decouple.config = decouple.Config(decouple.RepositoryEnv("./dev.env"))

from app.src.commons.constants.constants import APP_CONST

# ===========================================================================================
# Fast API App
# Dev: anh.vu
# ===========================================================================================

"""
    Cấu hình riêng cho fastapi app. Các thành phần:
"""

# ===========================================================================================

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi_health import health
from starlette.staticfiles import StaticFiles

from app.libs.exception.exceptions import handle_exception
from app.libs.exception.soa_error import SOA

# Declare element ===========================================================================

def healthy_condition():
    """ Trả về kết quả để kiểm tra hệ thống vẫn hoạt động bình thường """
    return {"service": "online"}


def sick_condition():
    """ Kiếm tra ứng dụng có hoạt động bình thường không """
    return True

# Main ======================================================================================
app = FastAPI(
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="libs/fastapi/static"), name="static")

app.add_api_route("/actuator/health", health([healthy_condition, sick_condition]))

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
        CUSTOM SWAGGER UI HTML
        Deploy lên K8s không có mạng vẫn có giao diện swagger
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - AV UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - AV ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

# Function help =============================================================================
def add_router(application, prefix_path, routers):
    """
        Thêm các route vào app
    """
    for router in routers:
        application.include_router(
            router=router.router,
            prefix=prefix_path,
            tags=router.tags
        )

# ===========================================================================================
# Application
# Dev: anh.vu
# ===========================================================================================

"""
    Khởi tạo ứng dụng và thêm các controller
"""

# ===========================================================================================

from fastapi.middleware.cors import CORSMiddleware

from app.src.commons.constants.constants import APP_CONST
from app.src.controllers.user_controller import user_controller
from app.src.controllers.config_controller import config_controller
from app.src.controllers.order_controller import order_controller

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
    order_controller,
    user_controller,
    config_controller
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



# Main ======================================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=APP_CONST.HOST,
        port=APP_CONST.PORT,
        log_level=APP_CONST.LOG_LEVEL,
        reload=True  # Tắt reload khi chạy dưới dạng dịch vụ
    )