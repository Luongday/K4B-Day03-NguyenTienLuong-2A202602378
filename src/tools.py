"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any


# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    # {
    #     "name": "academic_query",
    #     "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "student_id": {
    #                 "type": "string",
    #                 "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
    #             }
    #         },
    #         "required": ["student_id"]
    #     }
    # },
    {
        "name": "order_query",
        "description": "Tra cứu thông tin đơn hàng theo mã đơn hàng, bao gồm mã vận đơn, vị trí lưu kho và trạng thái hiện tại.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng cần tra cứu (ví dụ: 'ORD2026001')."
                }
            },
            "required": ["order_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    # {
    #     #     "name": "schedule_appointment",
    #     #     "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
    #     #     "parameters": {
    #     #         "type": "object",
    #     #         "properties": {
    #     #             # TODO 1.2: Khai báo các thuộc tính tham số cho Tool tại đây...
    #     #             "student_id": {
    #     #                 "type": "string",
    #     #                 "description": 'SV2026002'
    #     #             },
    #     #             "datetime_str" : {
    #     #                 "type": "string",
    #     #                 "description": '20:00 15/09/2026'
    #     #             },
    #     #             "advisor_name": {
    #     #                 "type": "string",
    #     #                 "description": 'Kill And Tea'
    #     #             }
    #     #         },
    #     #         "required": [
    #     #             "student_id",
    #     #             "datetime_str",
    #     #             "advisor_name"
    #     #         ] # TODO 1.2: Khai báo danh sách các trường bắt buộc tại đây...
    #     #     }
    #     # }
        {
        "name": "update_order_status",
        "description": "Cập nhật trạng thái xử lý hoặc vận chuyển của một đơn hàng trong hệ thống kho vận.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng cần cập nhật (ví dụ: 'ORD2026001')."
                },
                "new_status": {
                    "type": "string",
                    "description": "Trạng thái mới của đơn hàng, ví dụ: 'Đã đóng gói', 'Đang vận chuyển', 'Đã giao'."
                }
            },
            "required": ["order_id", "new_status"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

# MOCK_DATABASE = {
#     "SV2026001": {
#         "full_name": "Nguyễn Văn An",
#         "class": "AI-K4",
#         "gpa": 3.85,
#         "email": "an.nv@vinuni.edu.vn",
#         "status": "Đang học",
#         "advisor": "PGS.TS Nguyễn Văn A"
#     },
#     "SV2026002": {
#         "full_name": "Trần Thị Bình",
#         "class": "AI-K4",
#         "gpa": 3.60,
#         "email": "binh.tt@vinuni.edu.vn",
#         "status": "Đang học",
#         "advisor": "TS. Lê Thị B"
#     }
# }

MOCK_DATABASE = {
    "ORD2026001": {
        "tracking_code": "VNPOST-260001",
        "warehouse_location": "Kho Hà Nội - Kệ A12",
        "status": "Đang xử lý",
        "recipient": "Nguyễn Văn An"
    },
    "ORD2026002": {
        "tracking_code": "GHN-260002",
        "warehouse_location": "Kho Hà Nội - Kệ B07",
        "status": "Đã đóng gói",
        "recipient": "Trần Thị Bình"
    },
    "ORD2026003": {
        "tracking_code": "GHTK-260003",
        "warehouse_location": "Kho TP.HCM - Kệ C03",
        "status": "Đang vận chuyển",
        "recipient": "Lê Minh Khang"
    }
}

# def execute_academic_query(student_id: str) -> str:
#     """Thực thi tra cứu học vụ theo mã sinh viên"""
#     student = MOCK_DATABASE.get(student_id.strip().upper())
#     if student:
#         return json.dumps({
#             "status": "SUCCESS",
#             "student_id": student_id,
#             "data": student
#         }, ensure_ascii=False)
#     else:
#         return json.dumps({
#             "status": "NOT_FOUND",
#             "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
#         }, ensure_ascii=False)
#
#
# def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
#     """Thực thi đặt lịch hẹn tư vấn học vụ"""
#     return json.dumps({
#         "status": "SUCCESS",
#         "booking_id": f"BK-{student_id}-99",
#         "student_id": student_id,
#         "datetime": datetime_str,
#         "advisor": advisor_name,
#         "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
#     }, ensure_ascii=False)
#
#
# # Router gọi tool thực tế
# TOOL_ROUTER = {
#     "academic_query": execute_academic_query,
#     "schedule_appointment": execute_schedule_appointment
# }
#
# def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
#     """Hàm trung chuyển thực thi tool"""
#     if tool_name in TOOL_ROUTER:
#         try:
#             return TOOL_ROUTER[tool_name](**arguments)
#         except Exception as e:
#             return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
#     return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
def execute_order_query(order_id: str) -> str:
    """Tra cứu thông tin đơn hàng theo mã đơn hàng."""
    normalized_id = order_id.strip().upper()
    order = MOCK_DATABASE.get(normalized_id)

    if order:
        return json.dumps({
            "status": "SUCCESS",
            "order_id": normalized_id,
            "data": order
        }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "order_id": normalized_id,
        "message": f"Không tìm thấy đơn hàng có mã '{normalized_id}'."
    }, ensure_ascii=False)


def execute_update_order_status(order_id: str, new_status: str) -> str:
    """Cập nhật trạng thái đơn hàng."""
    normalized_id = order_id.strip().upper()
    order = MOCK_DATABASE.get(normalized_id)

    if not order:
        return json.dumps({
            "status": "NOT_FOUND",
            "order_id": normalized_id,
            "message": f"Không thể cập nhật vì không tìm thấy đơn hàng '{normalized_id}'."
        }, ensure_ascii=False)

    cleaned_status = new_status.strip()
    if not cleaned_status:
        return json.dumps({
            "status": "VALIDATION_ERROR",
            "order_id": normalized_id,
            "message": "Trạng thái mới không được để trống."
        }, ensure_ascii=False)

    old_status = order["status"]
    order["status"] = cleaned_status

    return json.dumps({
        "status": "SUCCESS",
        "order_id": normalized_id,
        "old_status": old_status,
        "new_status": cleaned_status,
        "message": (
            f"Đã cập nhật đơn hàng {normalized_id} từ trạng thái "
            f"'{old_status}' sang '{cleaned_status}'."
        )
    }, ensure_ascii=False)


TOOL_ROUTER = {
    "order_query": execute_order_query,
    "update_order_status": execute_update_order_status
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Trung chuyển yêu cầu từ MCP Server đến execution function tương ứng."""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({
                "status": "EXECUTION_ERROR",
                "error": str(e)
            }, ensure_ascii=False)

    return json.dumps({
        "status": "UNKNOWN_TOOL",
        "error": f"Tool '{tool_name}' không tồn tại!"
    }, ensure_ascii=False)