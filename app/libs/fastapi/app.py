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
        title=app.title + " - ECM Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ECM ReDoc",
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