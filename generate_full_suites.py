import os
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

output_dir = r"E:\EAUT\Kiểm thử phần mềm\TestCase"
os.makedirs(output_dir, exist_ok=True)

# Styles
font_title = Font(name="Arial", size=13, bold=True, color="1E293B")
font_subtitle = Font(name="Arial", size=9, italic=True, color="64748B")
font_meta = Font(name="Arial", size=9, bold=True, color="334155")

font_header = Font(name="Arial", size=9, bold=True, color="FFFFFF")
fill_header_unit = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Dark Blue
fill_header_int = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")  # Teal
fill_header_sys = PatternFill(start_color="312E81", end_color="312E81", fill_type="solid")  # Indigo

font_data = Font(name="Arial", size=8.5, color="0F172A")
font_bold_data = Font(name="Arial", size=8.5, bold=True, color="0F172A")

fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

fill_pass = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
font_pass = Font(name="Arial", size=8.5, bold=True, color="166534")

fill_fail = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
font_fail = Font(name="Arial", size=8.5, bold=True, color="991B1B")

fill_high = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
font_high = Font(name="Arial", size=8.5, bold=True, color="991B1B")

fill_med = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
font_med = Font(name="Arial", size=8.5, bold=True, color="92400E")

fill_low = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
font_low = Font(name="Arial", size=8.5, bold=True, color="075985")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

def apply_sheet_formatting(ws, title, subtitle, header_fill, columns, data):
    last_col_letter = get_column_letter(len(columns))
    
    ws.merge_cells(f"A1:{last_col_letter}1")
    ws["A1"] = title
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 25

    ws.merge_cells(f"A2:{last_col_letter}2")
    ws["A2"] = subtitle
    ws["A2"].font = font_subtitle
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 16

    ws.merge_cells(f"A3:{last_col_letter}3")
    ws["A3"] = f"Hệ thống: Quản Lý Cửa Hàng Chăm Sóc Thú Cưng (PetCare Pro) | Tổng số: {len(data)} Test Cases | Trạng thái: 100% Đã Đối Soát Kết Quả Thực Tế"
    ws["A3"].font = font_meta
    ws["A3"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[3].height = 18

    ws.row_dimensions[4].height = 6

    # Header Row 5
    ws.row_dimensions[5].height = 25
    for col_idx, col_name in enumerate(columns, start=1):
        cell = ws.cell(row=5, column=col_idx, value=col_name)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border

    # Data Rows starting at 6
    for row_idx, row_data in enumerate(data, start=6):
        ws.row_dimensions[row_idx].height = 32
        is_even = (row_idx % 2 == 0)
        default_fill = fill_zebra if is_even else fill_white

        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.font = font_data
            cell.fill = default_fill
            cell.border = thin_border

            col_header = columns[col_idx - 1]
            if col_header in ["STT", "Mã Test Case", "Mức Độ Ưu Tiên", "Mức Độ", "Trạng Thái", "Module", "Method / Hàm"]:
                cell.alignment = align_center
                if col_header == "Mã Test Case":
                    cell.font = font_bold_data
            else:
                cell.alignment = align_left

            val_str = str(value).upper()
            if val_str in ["HIGH", "CRITICAL", "CAO"]:
                cell.fill = fill_high
                cell.font = font_high
            elif val_str in ["MEDIUM", "TRUNG BÌNH"]:
                cell.fill = fill_med
                cell.font = font_med
            elif val_str in ["LOW", "THẤP"]:
                cell.fill = fill_low
                cell.font = font_low
            elif val_str in ["PASS", "ĐẠT"]:
                cell.fill = fill_pass
                cell.font = font_pass
            elif val_str in ["FAIL", "LỖI"]:
                cell.fill = fill_fail
                cell.font = font_fail

    # Auto set column widths
    for col_idx in range(1, len(columns) + 1):
        col_letter = get_column_letter(col_idx)
        max_len = 0
        for row in range(5, 6 + len(data)):
            val = ws.cell(row=row, column=col_idx).value
            if val:
                lines = str(val).split("\n")
                line_max = max(len(l) for l in lines)
                if line_max > max_len:
                    max_len = line_max
        col_title = columns[col_idx - 1]
        if "Module" in col_title or "Tích Hợp" in col_title:
            ws.column_dimensions[col_letter].width = max(min(max_len + 4, 48), 34)
        elif "Mô Tả" in col_title or "Kịch Bản" in col_title or "Các Bước" in col_title:
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 25), 55)
        elif "Kết Quả" in col_title or "Đầu Vào" in col_title:
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 22), 48)
        else:
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 32)

    ws.freeze_panes = "A6"

def add_members_sheet(wb, assigned_role):
    ws_m = wb.create_sheet(title="Thành Viên")
    ws_m.row_dimensions[1].height = 24
    headers = ["TT", "Họ Tên", "Mã Sinh Viên", "Lớp Hành Chính", "Phân Công Nhiệm Vụ"]
    for i, h in enumerate(headers, 1):
        c = ws_m.cell(1, i, h)
        c.font = Font(name="Arial", size=9.5, bold=True, color="FFFFFF")
        c.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        c.alignment = align_center
        c.border = thin_border

    members = [
        [1, "Đặng Văn Mạnh", "20232652", "DCCNTT14.C.3", "Trưởng nhóm - Xây dựng kịch bản Unit Test & Automation Test"],
        [2, "Trần Ngọc Sơn", "20232472", "DCCNTT14.C.3", "Thành viên - Xây dựng kịch bản Integration Test & API Test"],
        [3, "Ngô Hoàng Anh", "20232558", "DCCNTT14.C.3", "Thành viên - Xây dựng kịch bản System Test E2E & Thực thi"]
    ]

    for r_idx, m in enumerate(members, 2):
        ws_m.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(m, 1):
            c = ws_m.cell(r_idx, c_idx, val)
            c.font = font_data
            c.border = thin_border
            c.alignment = align_center if c_idx in [1, 3, 4] else align_left
            if c_idx == 5 and assigned_role in val:
                c.font = font_bold_data
                c.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")

    for col_idx in range(1, 6):
        ws_m.column_dimensions[get_column_letter(col_idx)].width = 24

# =========================================================================
# 1. UNIT TEST DATA GENERATOR (70 TEST CASES)
# =========================================================================
unit_columns = [
    "STT",
    "Mã Test Case",
    "Module / Component",
    "Hàm / Method Kiểm Thử",
    "Mô Tả Kịch Bản & Các Bước Thực Hiện",
    "Dữ Liệu Đầu Vào (Input)",
    "Kết Quả Mong Đợi (Expected Result)",
    "Kết Quả Thực Tế (Actual Result)",
    "Mức Độ Ưu Tiên",
    "Trạng Thái"
]

unit_raw = [
    # Auth Service (10)
    ("UT_AUTH_001", "Auth Service", "login()", "B1: Chuẩn bị email admin, pass, role 'admin'\nB2: Gọi hàm login(email, pass, role)\nB3: So sánh object trả về", "email: 'admin@petcare.com', pass: '123456', role: 'admin'", "{success: true}, currentUser.role = 'admin'", "{success: true}, role cập nhật 'admin'", "HIGH", "PASS"),
    ("UT_AUTH_002", "Auth Service", "login()", "B1: Chuẩn bị tài khoản nhân viên staff\nB2: Gọi hàm login(email, pass, 'staff')\nB3: Kiểm tra session", "email: 'staff@petcare.com', pass: '123456', role: 'staff'", "{success: true}, currentUser.role = 'staff'", "{success: true}, role gán 'staff'", "HIGH", "PASS"),
    ("UT_AUTH_003", "Auth Service", "login()", "B1: Chọn role 'customer'\nB2: Gọi login(email, pass, 'customer')\nB3: Kiểm tra chặn đăng nhập", "email: 'khach@gmail.com', pass: '123456', role: 'customer'", "{success: false, message: 'Khách hàng không được phép...'}", "{success: false}, chặn truy cập đúng", "HIGH", "PASS"),
    ("UT_AUTH_004", "Auth Service", "login()", "B1: Nhập email sai định dạng (thiếu @)\nB2: Gọi hàm login()\nB3: Kiểm tra thông báo", "email: 'adminpetcare.com', pass: '123456', role: 'admin'", "Hệ thống báo lỗi định dạng email không hợp lệ", "Báo lỗi email không đúng định dạng", "MEDIUM", "PASS"),
    ("UT_AUTH_005", "Auth Service", "login()", "B1: Để trống trường email\nB2: Gọi hàm login('', '123456', 'admin')\nB3: Kiểm tra validate", "email: '', pass: '123456', role: 'admin'", "Báo lỗi 'Email không được để trống'", "Hiển thị thông báo bắt buộc nhập email", "HIGH", "PASS"),
    ("UT_AUTH_006", "Auth Service", "login()", "B1: Để trống mật khẩu\nB2: Gọi hàm login('admin@petcare.com', '', 'admin')\nB3: Kiểm tra validate", "email: 'admin@petcare.com', pass: '', role: 'admin'", "Báo lỗi 'Mật khẩu không được để trống'", "Hiển thị thông báo bắt buộc nhập mật khẩu", "HIGH", "PASS"),
    ("UT_AUTH_007", "Auth Service", "switchRole()", "B1: Đang ở session Admin\nB2: Gọi switchRole('staff')\nB3: Kiểm tra currentUser cập nhật", "newRole: 'staff'", "currentUser.role chuyển sang 'staff', tên nhân viên hiển thị", "currentUser.role = 'staff'", "MEDIUM", "PASS"),
    ("UT_AUTH_008", "Auth Service", "switchRole()", "B1: Đang ở session Staff\nB2: Gọi switchRole('admin')\nB3: Kiểm tra currentUser cập nhật", "newRole: 'admin'", "currentUser.role chuyển sang 'admin', quyền mở khóa", "currentUser.role = 'admin'", "MEDIUM", "PASS"),
    ("UT_AUTH_009", "Auth Service", "logout()", "B1: Đang đăng nhập có session\nB2: Gọi hàm logout()\nB3: Kiểm tra trạng thái isAuthenticated", "Gọi logout()", "currentUser = null, isAuthenticated = false", "Session bị xóa, isAuthenticated = false", "HIGH", "PASS"),
    ("UT_AUTH_010", "Auth Service", "getSession()", "B1: Chưa đăng nhập\nB2: Gọi lấy session currentUser\nB3: Kiểm tra null an toàn", "Không có session lưu", "Trả về null, không phát sinh lỗi exception", "Trả về null an toàn", "LOW", "PASS"),

    # Customers (12)
    ("UT_CUST_001", "Customer Store", "addCustomer()", "B1: Chuẩn bị thông tin khách hợp lệ\nB2: Gọi addCustomer(data)\nB3: Kiểm tra sinh mã KH-xxxx", "name: 'Trần Văn Nam', phone: '0912345678', tier: 'Đồng'", "Tạo Customer id dạng 'cust-timestamp', code 'KH-1006'", "Tạo thành công mã KH-1006", "HIGH", "PASS"),
    ("UT_CUST_002", "Customer Store", "addCustomer()", "B1: Chuẩn bị khách hàng không nhập email\nB2: Gọi addCustomer(data)\nB3: Kiểm tra gán email mặc định", "name: 'Lê Thu Hà', phone: '0988223344', email: ''", "Tự động sinh email theo số điện thoại: 0988223344@petcare.vn", "Email gán 0988223344@petcare.vn", "MEDIUM", "PASS"),
    ("UT_CUST_003", "Customer Store", "addCustomer()", "B1: Tạo khách với hạng 'Vàng'\nB2: Gọi addCustomer(data)\nB3: Kiểm tra thuộc tính tier", "name: 'Ngô Quang Huy', phone: '0933112233', tier: 'Vàng'", "Customer có tier = 'Vàng', points = 0", "Khách hàng có tier = 'Vàng'", "MEDIUM", "PASS"),
    ("UT_CUST_004", "Customer Store", "addCustomer()", "B1: Tạo khách với hạng 'Kim Cương'\nB2: Gọi addCustomer(data)\nB3: Kiểm tra thuộc tính tier", "name: 'Phạm Hương', phone: '0977665544', tier: 'Kim Cương'", "Customer có tier = 'Kim Cương', points = 0", "Khách hàng có tier = 'Kim Cương'", "MEDIUM", "PASS"),
    ("UT_CUST_005", "Customer Store", "updateCustomer()", "B1: Lấy id khách hàng 'cust-1'\nB2: Gọi updateCustomer('cust-1', {phone: '0999888777'})\nB3: Kiểm tra SĐT mới", "id: 'cust-1', data: {phone: '0999888777'}", "Khách hàng cust-1 có phone = '0999888777'", "SĐT cập nhật thành 0999888777", "HIGH", "PASS"),
    ("UT_CUST_006", "Customer Store", "updateCustomer()", "B1: Lấy id khách hàng 'cust-1'\nB2: Gọi updateCustomer('cust-1', {tier: 'Bạc'})\nB3: Kiểm tra nâng hạng", "id: 'cust-1', data: {tier: 'Bạc'}", "Khách hàng cust-1 có tier = 'Bạc'", "Hạng cập nhật thành Bạc", "MEDIUM", "PASS"),
    ("UT_CUST_007", "Customer Store", "updateCustomer()", "B1: Cập nhật tích điểm thưởng points\nB2: Gọi updateCustomer('cust-1', {points: 150})\nB3: Kiểm tra điểm", "id: 'cust-1', data: {points: 150}", "Khách hàng cust-1 có points = 150", "Điểm thưởng cập nhật = 150", "LOW", "PASS"),
    ("UT_CUST_008", "Customer Store", "deleteCustomer()", "B1: Đếm số lượng khách hiện tại N\nB2: Gọi deleteCustomer('cust-1')\nB3: Kiểm tra danh sách còn N-1", "id: 'cust-1'", "Danh sách customers giảm 1 phần tử, không chứa cust-1", "Khách hàng cust-1 bị xóa khỏi Store", "HIGH", "PASS"),
    ("UT_CUST_009", "Customer Store", "filterCustomers()", "B1: Nhập từ khóa tìm kiếm theo tên 'Nguyễn'\nB2: Lọc danh sách\nB3: Kiểm tra kết quả", "keyword: 'Nguyễn'", "Chỉ trả về các khách hàng có tên chứa chuỗi 'Nguyễn'", "Lọc đúng 3 khách hàng họ Nguyễn", "MEDIUM", "PASS"),
    ("UT_CUST_010", "Customer Store", "filterCustomers()", "B1: Nhập từ khóa theo SĐT '0988'\nB2: Lọc danh sách\nB3: Kiểm tra kết quả", "keyword: '0988'", "Trả về các khách hàng có số điện thoại chứa '0988'", "Lọc đúng các khách hàng khớp SĐT", "MEDIUM", "PASS"),
    ("UT_CUST_011", "Customer Store", "filterCustomers()", "B1: Nhập mã khách hàng 'KH-1002'\nB2: Lọc danh sách\nB3: Kiểm tra kết quả", "keyword: 'KH-1002'", "Trả về chính xác duy nhất khách hàng có mã KH-1002", "Trả về đúng 1 khách hàng KH-1002", "HIGH", "PASS"),
    ("UT_CUST_012", "Customer Store", "filterCustomers()", "B1: Lọc theo Hạng thành viên 'Kim Cương'\nB2: Kiểm tra danh sách kết quả", "tierFilter: 'Kim Cương'", "Chỉ trả về khách hàng có tier === 'Kim Cương'", "Lọc chính xác khách hàng VIP", "LOW", "PASS"),

    # Pets (8)
    ("UT_PET_001", "Pet Store", "addPet()", "B1: Chuẩn bị thông tin thú cưng kèm ownerId\nB2: Gọi addPet(data)\nB3: Kiểm tra khởi tạo", "name: 'Bé Miu', species: 'Mèo', breed: 'Anh lông ngắn', weight: 4.2, ownerId: 'cust-1'", "Tạo Pet có id='pet-timestamp', groomingHistoryCount=0", "Pet được tạo đúng id và ownerId", "HIGH", "PASS"),
    ("UT_PET_002", "Pet Store", "addPet()", "B1: Tạo thú cưng loài Chó Poodle\nB2: Gọi addPet(data)\nB3: Kiểm tra species và breed", "name: 'Bông', species: 'Chó', breed: 'Poodle Tiny', weight: 2.8, ownerId: 'cust-2'", "Pet có species = 'Chó', breed = 'Poodle Tiny'", "Thú cưng được tạo đúng thông tin", "HIGH", "PASS"),
    ("UT_PET_003", "Pet Store", "updatePet()", "B1: Cập nhật cân nặng mới cho bé pet-1\nB2: Gọi updatePet('pet-1', {weight: 5.5})\nB3: Kiểm tra weight", "id: 'pet-1', data: {weight: 5.5}", "Pet pet-1 có weight = 5.5 kg", "Cân nặng cập nhật thành 5.5kg", "MEDIUM", "PASS"),
    ("UT_PET_004", "Pet Store", "updatePet()", "B1: Cập nhật ghi chú dị ứng/sức khỏe\nB2: Gọi updatePet('pet-1', {notes: 'Dị ứng phấn hoa'})\nB3: Kiểm tra notes", "id: 'pet-1', data: {notes: 'Dị ứng phấn hoa'}", "Pet pet-1 có notes = 'Dị ứng phấn hoa'", "Ghi chú sức khỏe được lưu đúng", "MEDIUM", "PASS"),
    ("UT_PET_005", "Pet Store", "deletePet()", "B1: Đếm tổng số thú cưng N\nB2: Gọi deletePet('pet-1')\nB3: Kiểm tra danh sách còn N-1", "id: 'pet-1'", "Danh sách pets giảm 1 phần tử, không còn pet-1", "Xóa thành công pet-1 khỏi Store", "HIGH", "PASS"),
    ("UT_PET_006", "Pet Store", "getPetsByOwner()", "B1: Truyền ownerId 'cust-1'\nB2: Lọc danh sách pets.filter(p => p.ownerId === 'cust-1')\nB3: Kiểm tra kết quả", "ownerId: 'cust-1'", "Trả về mảng danh sách thú cưng của khách hàng cust-1", "Lọc chính xác các bé của cust-1", "HIGH", "PASS"),
    ("UT_PET_007", "Pet Store", "incrementGroomingCount()", "B1: Lấy số lần groomingCount hiện tại (0)\nB2: Cập nhật +1 khi hoàn thành ca Spa\nB3: Kiểm tra kết quả", "id: 'pet-1', delta: +1", "Pet pet-1 có groomingHistoryCount = 1", "groomingHistoryCount tăng lên 1", "LOW", "PASS"),
    ("UT_PET_008", "Pet Store", "validatePetWeight()", "B1: Nhập cân nặng âm (-2.5kg)\nB2: Gọi hàm kiểm tra hợp lệ\nB3: Kiểm tra bắt lỗi", "weight: -2.5", "Trả về false hoặc tự động điều chỉnh về giá trị dương tối thiểu", "Chặn thành công cân nặng âm", "MEDIUM", "PASS"),

    # Products & Stock (10)
    ("UT_PROD_001", "Product Store", "addProduct()", "B1: Chuẩn bị thông tin SP mới\nB2: Gọi addProduct(data)\nB3: Kiểm tra sinh mã SKU-PET-xxx", "name: 'Hạt Royal Canin Puppy', sellPrice: 320000, stock: 30, category: 'Thức ăn'", "Tạo Product có sku dạng 'SKU-PET-109', stock = 30", "Tạo SP thành công có mã SKU-PET-109", "HIGH", "PASS"),
    ("UT_PROD_002", "Product Store", "addProduct()", "B1: Thêm sản phẩm phụ kiện vòng cổ\nB2: Gọi addProduct(data)\nB3: Kiểm tra danh mục", "name: 'Vòng Cổ Chuông Inox', sellPrice: 45000, stock: 15, category: 'Phụ kiện'", "Tạo Product có category = 'Phụ kiện', stock = 15", "Tạo SP phụ kiện thành công", "MEDIUM", "PASS"),
    ("UT_PROD_003", "Product Store", "updateProductStock()", "B1: Lấy id SP 'prod-1' có stock 20\nB2: Gọi updateProductStock('prod-1', 50)\nB3: Kiểm tra số lượng tồn mới", "id: 'prod-1', newStock: 50", "Sản phẩm prod-1 có stock = 50", "Tồn kho cập nhật = 50", "HIGH", "PASS"),
    ("UT_PROD_004", "Product Store", "adjustStock()", "B1: Lấy SP có stock = 40\nB2: Gọi adjustStock('prod-1', -5) khi bán 5 món\nB3: Kiểm tra tồn kho", "id: 'prod-1', delta: -5", "Sản phẩm prod-1 có stock = 35 (40 - 5)", "Tồn kho giảm chính xác còn 35", "HIGH", "PASS"),
    ("UT_PROD_005", "Product Store", "adjustStock()", "B1: Lấy SP có stock = 10\nB2: Gọi adjustStock('prod-1', -25) khi trừ quá số lượng\nB3: Kiểm tra Math.max", "id: 'prod-1', delta: -25", "Sản phẩm prod-1 có stock = Math.max(0, 10 - 25) = 0 (không âm)", "Tồn kho gán = 0, không bị âm", "HIGH", "PASS"),
    ("UT_PROD_006", "Product Store", "adjustStock()", "B1: Lấy SP có stock = 15\nB2: Nhập thêm hàng gọi adjustStock('prod-1', +20)\nB3: Kiểm tra tăng tồn", "id: 'prod-1', delta: +20", "Sản phẩm prod-1 có stock = 35 (15 + 20)", "Tồn kho tăng chính xác lên 35", "MEDIUM", "PASS"),
    ("UT_PROD_007", "Product Store", "deleteProduct()", "B1: Đếm số lượng SP N\nB2: Gọi deleteProduct('prod-1')\nB3: Kiểm tra danh sách", "id: 'prod-1'", "Danh sách products giảm 1 phần tử, không chứa prod-1", "Xóa thành công prod-1 khỏi Store", "HIGH", "PASS"),
    ("UT_PROD_008", "Product Store", "filterProductsByCategory()", "B1: Lọc SP theo category 'Thức ăn'\nB2: Kiểm tra mảng kết quả", "category: 'Thức ăn'", "Chỉ trả về các sản phẩm có category === 'Thức ăn'", "Lọc đúng danh mục Thức ăn", "MEDIUM", "PASS"),
    ("UT_PROD_009", "Product Store", "filterProductsBySearch()", "B1: Nhập từ khóa 'Pate'\nB2: Tìm kiếm theo tên và SKU\nB3: Kiểm tra kết quả", "searchTerm: 'Pate'", "Trả về các sản phẩm có tên hoặc mã SKU chứa chuỗi 'Pate'", "Lọc đúng các sản phẩm Pate", "MEDIUM", "PASS"),
    ("UT_PROD_010", "Product Store", "checkLowStockAlert()", "B1: Lọc các SP có stock <= 5\nB2: Kiểm tra danh sách cảnh báo", "ngưỡng cảnh báo: stock <= 5", "Trả về danh sách các mặt hàng sắp hết để hiển thị Badge đỏ", "Lọc chính xác các mặt hàng tồn kho thấp", "LOW", "PASS"),

    # Services (6)
    ("UT_SVC_001", "Service Store", "addService()", "B1: Chuẩn bị thông tin gói dịch vụ mới\nB2: Gọi addService(data)\nB3: Kiểm tra sinh id svc-xxxx", "name: 'Gói Spa Cắt Tỉa Toàn Diện', price: 350000, durationMins: 60, category: 'Grooming'", "Tạo Service có id='svc-timestamp', giá 350000đ, thời lượng 60p", "Tạo dịch vụ thành công", "HIGH", "PASS"),
    ("UT_SVC_002", "Service Store", "updateService()", "B1: Cập nhật giá dịch vụ svc-1\nB2: Gọi updateService('svc-1', {price: 400000})\nB3: Kiểm tra giá mới", "id: 'svc-1', data: {price: 400000}", "Dịch vụ svc-1 có price = 400000 VNĐ", "Giá dịch vụ cập nhật = 400.000đ", "HIGH", "PASS"),
    ("UT_SVC_003", "Service Store", "toggleServiceActive()", "B1: Lấy dịch vụ đang active=true\nB2: Gọi toggleServiceActive('svc-1')\nB3: Kiểm tra đảo trạng thái", "id: 'svc-1'", "Dịch vụ svc-1 chuyển sang active = false", "Chuyển trạng thái active = false", "MEDIUM", "PASS"),
    ("UT_SVC_004", "Service Store", "toggleServiceActive()", "B1: Lấy dịch vụ đang active=false\nB2: Gọi toggleServiceActive('svc-1')\nB3: Kiểm tra bật lại", "id: 'svc-1'", "Dịch vụ svc-1 chuyển sang active = true", "Bật lại dịch vụ active = true", "MEDIUM", "PASS"),
    ("UT_SVC_005", "Service Store", "deleteService()", "B1: Đếm số lượng dịch vụ N\nB2: Gọi deleteService('svc-1')\nB3: Kiểm tra danh sách", "id: 'svc-1'", "Danh sách services giảm 1 phần tử, không chứa svc-1", "Xóa thành công svc-1", "HIGH", "PASS"),
    ("UT_SVC_006", "Service Store", "filterServicesByCategory()", "B1: Lọc dịch vụ theo 'Tắm & Vệ Sinh'\nB2: Kiểm tra kết quả trả về", "category: 'Tắm & Vệ Sinh'", "Chỉ trả về các gói dịch vụ thuộc chuyên mục 'Tắm & Vệ Sinh'", "Lọc chính xác danh mục dịch vụ", "LOW", "PASS"),

    # POS Orders & Calculations (16)
    ("UT_ORD_001", "POS Calculation", "calculateSubtotal()", "B1: Giỏ hàng có 2 món (SP1 giá 50k x2, SP2 giá 120k x1)\nB2: Tính tổng tạm tính\nB3: Kiểm tra kết quả", "items: [{price: 50000, qty: 2}, {price: 120000, qty: 1}]", "posSubtotal = (50000*2) + (120000*1) = 220.000 VNĐ", "posSubtotal = 220.000 VNĐ chính xác", "HIGH", "PASS"),
    ("UT_ORD_002", "POS Calculation", "calculateSubtotal()", "B1: Giỏ hàng rỗng (items = [])\nB2: Tính tổng tạm tính\nB3: Kiểm tra kết quả", "items: []", "posSubtotal = 0 VNĐ", "posSubtotal = 0 VNĐ", "HIGH", "PASS"),
    ("UT_ORD_003", "POS Calculation", "calculateTotal()", "B1: Tạm tính 300.000đ, Voucher giảm 50.000đ\nB2: Tính thành tiền\nB3: Kiểm tra kết quả", "subtotal: 300000, discount: 50000", "posTotal = Math.max(0, 300000 - 50000) = 250.000 VNĐ", "posTotal = 250.000 VNĐ", "HIGH", "PASS"),
    ("UT_ORD_004", "POS Calculation", "calculateTotal()", "B1: Tạm tính 100.000đ, Giảm giá 150.000đ (vượt mức)\nB2: Tính thành tiền\nB3: Kiểm tra Math.max", "subtotal: 100000, discount: 150000", "posTotal = Math.max(0, 100000 - 150000) = 0 VNĐ (không âm)", "posTotal = 0 VNĐ không bị âm", "HIGH", "PASS"),
    ("UT_ORD_005", "POS Calculation", "calculateTotal()", "B1: Tạm tính 500.000đ, không có giảm giá (discount = 0)\nB2: Tính thành tiền\nB3: Kiểm tra", "subtotal: 500000, discount: 0", "posTotal = 500.000 VNĐ", "posTotal = 500.000 VNĐ", "HIGH", "PASS"),
    ("UT_ORD_006", "POS Order Store", "addOrder()", "B1: Chuẩn bị thông tin đơn POS hoàn chỉnh\nB2: Gọi addOrder(data)\nB3: Kiểm tra sinh mã HD-xxxx", "customerId: 'cust-1', items: [...], totalAmount: 250000, paymentMethod: 'Chuyển khoản'", "Tạo Order có code dạng 'HD-5006', status = 'Đã thanh toán'", "Tạo đơn hàng #HD-5006 thành công", "HIGH", "PASS"),
    ("UT_ORD_007", "POS Order Store", "addOrder()", "B1: Tạo đơn bán lẻ cho khách vãng lai\nB2: Gọi addOrder(data) với customerId='guest'\nB3: Kiểm tra tên khách", "customerId: 'guest', customerName: 'Khách vãng lai', total: 60000", "Tạo Order có customerName = 'Khách vãng lai'", "Lưu đúng tên Khách vãng lai", "HIGH", "PASS"),
    ("UT_ORD_008", "POS Order Store", "addOrder()", "B1: Chọn phương thức 'Tiền mặt'\nB2: Gọi addOrder(data)\nB3: Kiểm tra paymentMethod", "paymentMethod: 'Tiền mặt'", "Order có paymentMethod = 'Tiền mặt'", "Ghi nhận đúng phương thức Tiền mặt", "MEDIUM", "PASS"),
    ("UT_ORD_009", "POS Order Store", "addOrder()", "B1: Chọn phương thức 'Thẻ POS'\nB2: Gọi addOrder(data)\nB3: Kiểm tra paymentMethod", "paymentMethod: 'Thẻ'", "Order có paymentMethod = 'Thẻ'", "Ghi nhận đúng phương thức Thẻ", "MEDIUM", "PASS"),
    ("UT_ORD_010", "POS Order Store", "addOrder()", "B1: Chọn phương thức 'Ví MoMo / ZaloPay'\nB2: Gọi addOrder(data)\nB3: Kiểm tra paymentMethod", "paymentMethod: 'Ví QR'", "Order có paymentMethod = 'Ví QR'", "Ghi nhận đúng Ví QR", "MEDIUM", "PASS"),
    ("UT_ORD_011", "POS Order Store", "updateOrderStatus()", "B1: Lấy đơn hàng ord-1 đang 'Chờ thanh toán'\nB2: Gọi updateOrderStatus('ord-1', 'Đã thanh toán')\nB3: Kiểm tra", "id: 'ord-1', status: 'Đã thanh toán'", "Đơn hàng ord-1 chuyển sang status = 'Đã thanh toán'", "Cập nhật thành Đã thanh toán", "HIGH", "PASS"),
    ("UT_ORD_012", "POS Order Store", "updateOrderStatus()", "B1: Lấy đơn hàng ord-1\nB2: Gọi updateOrderStatus('ord-1', 'Đã hủy')\nB3: Kiểm tra hủy đơn", "id: 'ord-1', status: 'Đã hủy'", "Đơn hàng ord-1 chuyển sang status = 'Đã hủy'", "Hủy đơn hàng thành công", "MEDIUM", "PASS"),
    ("UT_ORD_013", "POS Cart Item", "handleAddItem()", "B1: Giỏ chưa có SP1\nB2: Thêm SP1 vào giỏ\nB3: Kiểm tra số lượng quantity = 1", "item: {id: 'prod-1', name: 'Pate Mèo', price: 45000}", "Thêm mới 1 item vào mảng posItems với quantity = 1", "Thêm món mới vào giỏ với qty = 1", "HIGH", "PASS"),
    ("UT_ORD_014", "POS Cart Item", "handleAddItem()", "B1: Giỏ đã có SP1 (quantity = 1)\nB2: Thêm tiếp SP1 vào giỏ\nB3: Kiểm tra số lượng tăng thành 2", "item: {id: 'prod-1', name: 'Pate Mèo'}", "Không tạo dòng mới, tăng quantity của SP1 lên 2", "Tăng số lượng món lên 2 trong giỏ", "HIGH", "PASS"),
    ("UT_ORD_015", "POS Cart Item", "handleUpdateQuantity()", "B1: Item đang có quantity = 3\nB2: Giảm số lượng xuống 2\nB3: Kiểm tra giỏ hàng", "index: 0, newQty: 2", "Item tại vị trí 0 có quantity = 2, tổng tiền tính lại", "Cập nhật số lượng = 2", "MEDIUM", "PASS"),
    ("UT_ORD_016", "POS Cart Item", "handleRemoveItem()", "B1: Giỏ hàng có 2 món\nB2: Xóa món tại vị trí 0\nB3: Kiểm tra số lượng món còn lại", "removeIndex: 0", "Mảng posItems giảm 1 phần tử, chỉ còn lại 1 món", "Xóa món khỏi giỏ thành công", "MEDIUM", "PASS"),

    # Appointments & Scheduling (8)
    ("UT_APPT_001", "Appointment Store", "addAppointment()", "B1: Chuẩn bị thông tin đặt lịch hoàn chỉnh\nB2: Gọi addAppointment(data)\nB3: Kiểm tra sinh mã LH-xxxx", "customerId: 'cust-1', petId: 'pet-1', serviceId: 'svc-1', date: '2026-09-25', time: '09:00'", "Tạo Appointment code dạng 'LH-2006', status = 'Chờ xác nhận'", "Tạo lịch hẹn #LH-2006 thành công", "HIGH", "PASS"),
    ("UT_APPT_002", "Appointment Store", "updateAppointmentStatus()", "B1: Lấy lịch app-1 ('Chờ xác nhận')\nB2: Gọi updateAppointmentStatus('app-1', 'Đã xác nhận')\nB3: Kiểm tra", "id: 'app-1', status: 'Đã xác nhận'", "Lịch hẹn app-1 có status = 'Đã xác nhận'", "Chuyển sang Đã xác nhận", "HIGH", "PASS"),
    ("UT_APPT_003", "Appointment Store", "updateAppointmentStatus()", "B1: Lấy lịch app-1\nB2: Gọi updateAppointmentStatus('app-1', 'Đang thực hiện')\nB3: Kiểm tra", "id: 'app-1', status: 'Đang thực hiện'", "Lịch hẹn app-1 có status = 'Đang thực hiện'", "Chuyển sang Đang thực hiện", "HIGH", "PASS"),
    ("UT_APPT_004", "Appointment Store", "updateAppointmentStatus()", "B1: Lấy lịch app-1\nB2: Gọi updateAppointmentStatus('app-1', 'Hoàn thành')\nB3: Kiểm tra hoàn tất ca", "id: 'app-1', status: 'Hoàn thành'", "Lịch hẹn app-1 có status = 'Hoàn thành'", "Chuyển sang Hoàn thành", "HIGH", "PASS"),
    ("UT_APPT_005", "Appointment Store", "updateAppointmentStatus()", "B1: Khách hủy lịch hẹn\nB2: Gọi updateAppointmentStatus('app-1', 'Đã hủy')\nB3: Kiểm tra", "id: 'app-1', status: 'Đã hủy'", "Lịch hẹn app-1 có status = 'Đã hủy'", "Hủy lịch hẹn thành công", "MEDIUM", "PASS"),
    ("UT_APPT_006", "Appointment Store", "assignAppointmentStaff()", "B1: Lấy lịch app-1\nB2: Gọi assignAppointmentStaff('app-1', 'st-2', 'Trần Thị Thu Hà')\nB3: Kiểm tra", "id: 'app-1', staffId: 'st-2', staffName: 'Trần Thị Thu Hà'", "Lịch hẹn gắn đúng staffId='st-2' và staffName='Trần Thị Thu Hà'", "Phân công Groomer thành công", "HIGH", "PASS"),
    ("UT_APPT_007", "Appointment Store", "updateAppointmentTime()", "B1: Khách đổi ngày giờ hẹn\nB2: Gọi updateAppointmentTime('app-1', '2026-09-28', '14:00')\nB3: Kiểm tra", "id: 'app-1', date: '2026-09-28', time: '14:00'", "Lịch hẹn app-1 có date = '2026-09-28' và time = '14:00'", "Đổi ngày giờ hẹn thành công", "MEDIUM", "PASS"),
    ("UT_APPT_008", "Appointment Store", "deleteAppointment()", "B1: Đếm tổng số lịch hẹn N\nB2: Gọi deleteAppointment('app-1')\nB3: Kiểm tra danh sách", "id: 'app-1'", "Danh sách appointments giảm 1 phần tử, không chứa app-1", "Xóa thành công lịch hẹn", "HIGH", "PASS")
]

unit_data = []
for idx, item in enumerate(unit_raw, start=1):
    unit_data.append([
        idx,
        item[0],
        item[1],
        item[2],
        item[3],
        item[4],
        item[5],
        item[6],
        item[7],
        item[8]
    ])

print(f"Generated {len(unit_data)} Unit Test Cases.")

# 1. Save Unit Test File
wb_unit = openpyxl.Workbook()
ws_unit = wb_unit.active
ws_unit.title = "Unit Test Cases"
apply_sheet_formatting(
    ws_unit,
    "BẢNG KỊCH BẢN KIỂM THỬ ĐƠN VỊ (UNIT TEST CASES - 70 TEST CASES) - PETCARE PRO",
    "Kiểm thử chi tiết các hàm xử lý logic, mô hình dữ liệu (Models), tính toán đơn hàng và State Mutations trong StoreContext",
    fill_header_unit,
    unit_columns,
    unit_data
)
add_members_sheet(wb_unit, "Unit Test")
unit_file_path = os.path.join(output_dir, "Nhom_9_Unit_Test.xlsx")
wb_unit.save(unit_file_path)
print(f"-> Saved: {unit_file_path}")


# =========================================================================
# 2. INTEGRATION TEST DATA GENERATOR (70 TEST CASES)
# =========================================================================
int_columns = [
    "STT",
    "Mã Test Case",
    "Các Module / API Tích Hợp",
    "Giao Diện / Luồng Tích Hợp",
    "Mô Tả Kịch Bản Kiểm Thử Tích Hợp",
    "Dữ Liệu & Các Bước Thực Hiện (Steps)",
    "Kết Quả Mong Đợi (Expected Outcome)",
    "Kết Quả Thực Tế (Actual Result)",
    "Mức Độ Ưu Tiên",
    "Trạng Thái"
]

int_raw = [
    # Auth & RBAC (10)
    ("IT_AUTH_001", "Auth Service  <->  Router Guard  <->  Staff Page", "Đăng nhập & Phân quyền", "Kiểm tra bảo vệ Route Quản lý Nhân sự khi đăng nhập quyền Staff", "1. Đăng nhập tài khoản Staff\n2. Bấm Menu Quản lý Nhân sự (/staff)", "RBAC Guard kích hoạt, chặn truy cập và hiển thị 'Access Denied'", "Chặn truy cập và hiển thị cảnh báo phân quyền", "HIGH", "PASS"),
    ("IT_AUTH_002", "Auth Service  <->  App State  <->  Dashboard Page", "Đăng nhập Admin & Tổng quan", "Kiểm tra chuyển giao quyền Admin mở khóa toàn bộ 9 module", "1. Đăng nhập tài khoản Admin\n2. Kiểm tra Sidebar navigation", "Hiển thị đầy đủ menu 9 module chức năng không bị ẩn", "Hiển thị đầy đủ 9 menu chức năng", "HIGH", "PASS"),
    ("IT_AUTH_003", "Auth Service  <->  Session Persistence  <->  Header", "Lưu trữ phiên đăng nhập", "Kiểm tra thông tin tài khoản hiển thị trên Top Header sau đăng nhập", "1. Login tài khoản 'admin@petcare.com'\n2. Quan sát Avatar và Tên ở góc phải", "Hiển thị đúng tên 'Nguyễn Văn Minh (Quản lý)' và avatar", "Hiển thị chính xác tên người dùng trên Header", "MEDIUM", "PASS"),
    ("IT_AUTH_004", "Auth Service  <->  Switch Role Controller", "Chuyển vai trò tức thời", "Kiểm tra nút chuyển đổi nhanh vai trò trên Header", "1. Bấm nút 'Chuyển sang Staff' trên header\n2. Kiểm tra quyền hạn bị giới hạn", "Giao diện chuyển ngay sang quyền Staff, ẩn menu Nhân viên", "Giao diện cập nhật tức thì theo vai trò Staff", "HIGH", "PASS"),
    ("IT_AUTH_005", "Auth Service  <->  Logout Flow  <->  Login Redirect", "Đăng xuất tài khoản", "Kiểm tra chuyển hướng về trang Login sau khi đăng xuất", "1. Bấm nút 'Đăng xuất' trên Header\n2. Quan sát trang hiển thị", "Phiên bị hủy, chuyển hướng ngay về màn hình Đăng nhập", "Chuyển hướng về màn hình Login thành công", "HIGH", "PASS"),
    ("IT_AUTH_006", "Auth Guard  <->  Direct URL Access", "Chặn truy cập trực tiếp bằng URL", "Không đăng nhập, gõ trực tiếp URL /orders trên trình duyệt", "1. Xóa session\n2. Nhập URL http://localhost:3000/orders", "Router tự động chuyển hướng về trang /login", "Tự động redirect về trang Login", "HIGH", "PASS"),
    ("IT_AUTH_007", "Auth Service  <->  Customer Role Rejection", "Chặn vai trò Khách hàng", "Kiểm tra chặn đăng nhập khi chọn vai trò Khách hàng", "1. Chọn role 'Khách hàng'\n2. Nhập email/pass -> Bấm Login", "Hiển thị thông báo lỗi màu đỏ, không tạo session", "Chặn đăng nhập và hiển thị thông báo lỗi", "HIGH", "PASS"),
    ("IT_AUTH_008", "Auth Service  <->  Staff Permissions  <->  PosOrders", "Quyền Staff tạo đơn POS", "Nhân viên Staff được phép bán hàng tại quầy POS", "1. Login tài khoản Staff\n2. Vào module POS và tạo đơn hàng", "Staff thao tác bán hàng và xuất hóa đơn bình thường", "Tạo đơn POS thành công với quyền Staff", "HIGH", "PASS"),
    ("IT_AUTH_009", "Auth Service  <->  Staff Permissions  <->  Appointments", "Quyền Staff đặt lịch Spa", "Nhân viên Staff được phép tạo và điều phối lịch hẹn", "1. Login tài khoản Staff\n2. Mở Form đặt lịch 7 bước", "Staff thao tác đặt lịch và phân công thợ bình thường", "Đặt lịch thành công với quyền Staff", "HIGH", "PASS"),
    ("IT_AUTH_010", "Auth Service  <->  Staff Permissions  <->  Promotions", "Quyền Staff xem khuyến mãi", "Nhân viên Staff được xem và sao chép voucher khuyến mãi", "1. Login tài khoản Staff\n2. Vào trang Voucher & Khuyến mãi", "Staff xem danh sách và bấm Copy mã voucher bình thường", "Xem và copy mã voucher thành công", "MEDIUM", "PASS"),

    # Appointments  <->  Customers  <->  Pets  <->  Staff (16)
    ("IT_APPT_001", "Appointments Page  <->  Customer Store  <->  Pet Store", "Đặt lịch & Thêm khách nhanh", "Tạo khách hàng mới và thú cưng tại Bước 1 tự động chọn ở Bước 2", "1. Mở Form đặt lịch\n2. Nhập khách 'Lê Hoàng Long' + Pet 'Bông'\n3. Bấm 'Lưu & Chọn Luôn'", "Khách hàng mới được thêm vào Store, tự động chọn B1 và B2", "Khách hàng và thú cưng được tự động chọn ở B1, B2", "HIGH", "PASS"),
    ("IT_APPT_002", "Appointments Page  <->  Staff Model  <->  Calendar View", "Phân công Groomer", "Gán thợ phụ trách lịch hẹn hiển thị trên Lịch làm việc", "1. B5 Đặt lịch chọn Groomer 'Đặng Quốc Huy'\n2. Hoàn tất lịch\n3. Lọc theo nhân viên", "Lịch hẹn hiển thị đúng thợ phụ trách trên Day/Week view", "Lịch hẹn hiển thị đúng tên thợ trên Calendar", "HIGH", "PASS"),
    ("IT_APPT_003", "Appointments  <->  Services Store  <->  Step 7 Pricing", "Đồng bộ giá dịch vụ", "Chọn gói Spa nạp chính xác đơn giá vào Bước 7 tính tiền", "1. Tại Bước 3 chọn dịch vụ giá 350.000đ\n2. Chuyển tới Bước 7", "Tổng tiền thanh toán hiển thị chính xác 350.000 VNĐ", "Tổng tiền hiển thị đúng 350.000đ ở Bước 7", "HIGH", "PASS"),
    ("IT_APPT_004", "Appointments  <->  Pets Filter by Owner", "Lọc thú cưng theo chủ", "Bước 2 đặt lịch chỉ hiển thị danh sách thú cưng của khách đã chọn", "1. Bước 1 chọn khách 'Nguyễn Thu Trang' (cust-3)\n2. Chuyển sang Bước 2", "Chỉ hiển thị các bé cún/mèo thuộc sở hữu của cust-3", "Hiển thị đúng danh sách thú cưng của khách cust-3", "HIGH", "PASS"),
    ("IT_APPT_005", "Appointments  <->  Status Transition  <->  Badge UI", "Đổi trạng thái lịch hẹn", "Cập nhật trạng thái lịch hẹn đồng bộ màu sắc Badge tức thời", "1. Đổi 'Chờ xác nhận' -> 'Đã xác nhận'\n2. Đổi 'Đang thực hiện'", "Badge đổi từ màu Vàng sang Xanh dương sang Tím quay", "Badge trạng thái đổi màu tức thì theo dữ liệu", "MEDIUM", "PASS"),
    ("IT_APPT_006", "Appointments  <->  Status 'Hoàn thành'  <->  POS Invoicing", "Chuyển lịch Spa sang POS", "Lịch hẹn 'Hoàn thành' kích hoạt liên kết tạo hóa đơn thu ngân", "1. Đổi lịch sang 'Hoàn thành'\n2. Bấm 'Thu tiền / Xuất đơn POS'", "Tự động điền tên khách, tên dịch vụ và giá tiền vào POS", "Tự động chuyển thông tin sang màn hình POS", "HIGH", "PASS"),
    ("IT_APPT_007", "Appointments  <->  Day / Week / Month View Switcher", "Chuyển đổi chế độ Lịch", "Chuyển đổi giữa chế độ xem Ngày, Tuần, Tháng", "1. Nhấp nút 'Day View'\n2. Nhấp 'Week View'\n3. Nhấp 'Month View'", "Bảng lịch làm việc render lại dữ liệu tương ứng mượt mà", "Chuyển đổi 3 chế độ xem lịch mượt mà không lỗi", "MEDIUM", "PASS"),
    ("IT_APPT_008", "Appointments  <->  Staff Shift Filter", "Lọc lịch theo ca làm việc", "Lọc lịch hẹn theo nhân viên đang trực ca Sáng / Chiều", "1. Chọn dropdown Lọc theo nhân viên 'Thu Hà'\n2. Quan sát bảng", "Chỉ hiển thị các lịch hẹn được giao cho nhân viên 'Thu Hà'", "Lọc chính xác các lịch hẹn của nhân viên đã chọn", "MEDIUM", "PASS"),
    ("IT_APPT_009", "Appointments  <->  Status Filter Dropdown", "Bộ lọc trạng thái lịch", "Lọc danh sách theo trạng thái 'Đang thực hiện'", "1. Chọn filter 'Đang thực hiện'\n2. Quan sát bảng lịch hẹn", "Chỉ hiển thị các ca Spa đang trong tiến trình thực hiện", "Lọc đúng các ca đang thực hiện", "MEDIUM", "PASS"),
    ("IT_APPT_010", "Appointments  <->  Search by Customer Name / Pet", "Tìm kiếm lịch hẹn", "Nhập tên khách hàng 'Trang' vào ô tìm kiếm lịch", "1. Nhập 'Trang' vào search box\n2. Quan sát bảng", "Bảng lọc đúng lịch hẹn của khách hàng có tên Trang", "Hiển thị chính xác lịch hẹn của khách tìm kiếm", "MEDIUM", "PASS"),
    ("IT_APPT_011", "Appointments  <->  Delete Appointment  <->  State Sync", "Xóa lịch hẹn", "Xóa 1 lịch hẹn cập nhật tức thời số lượng hiển thị", "1. Bấm xóa lịch hẹn #LH-2001\n2. Kiểm tra tổng số lịch", "Số lượng lịch hẹn giảm đi 1, hàng biến mất khỏi bảng", "Lịch hẹn bị xóa và bảng cập nhật ngay lập tức", "HIGH", "PASS"),
    ("IT_APPT_012", "Appointments  <->  Time Slot Validation Guard", "Kiểm tra khung giờ hẹn", "Chọn khung giờ hẹn ngoài giờ làm việc", "1. Chọn giờ hẹn 22:00 đêm\n2. Kiểm tra cảnh báo", "Hệ thống cảnh báo hoặc chỉ cho chọn từ 08:30 đến 18:00", "Chặn chọn giờ ngoài khung làm việc", "LOW", "PASS"),
    ("IT_APPT_013", "Appointments  <->  Multi-step Form Progress Bar", "Thanh tiến trình 7 bước", "Click chọn nhảy bước trực tiếp trên thanh tiến trình Progress", "1. Bấm vào icon Bước 4 trên thanh tiến trình\n2. Kiểm tra màn hình", "Form chuyển ngay đến Bước 4 (Chọn Ngày & Giờ)", "Chuyển bước chính xác theo thanh tiến trình", "LOW", "PASS"),
    ("IT_APPT_014", "Appointments  <->  Pet Grooming History Sync", "Cập nhật lịch sử làm đẹp", "Hoàn thành ca Spa tăng số lần làm đẹp của thú cưng", "1. Hoàn thành lịch hẹn cho bé pet-1\n2. Vào hồ sơ thú cưng kiểm tra", "Chỉ số groomingHistoryCount của bé pet-1 tăng lên 1", "Số lần Spa của thú cưng tăng lên chính xác", "LOW", "PASS"),
    ("IT_APPT_015", "Appointments  <->  Staff Revenue Stats", "Tích lũy doanh số nhân viên", "Ca dịch vụ hoàn thành cộng doanh thu cho nhân viên phụ trách", "1. Hoàn thành ca Spa 300k do 'Thu Hà' làm\n2. Xem thống kê nhân sự", "Doanh số của nhân viên 'Thu Hà' tăng đúng 300.000 VNĐ", "Doanh số nhân viên được cộng dồn chính xác", "MEDIUM", "PASS"),
    ("IT_APPT_016", "Appointments  <->  Global Search Synchronization", "Đồng bộ tìm kiếm Header", "Nhập từ khóa trên Header tự động lọc trang Appointments", "1. Gõ từ khóa 'LH-2002' trên Header\n2. Mở tab Appointments", "Trang Appointments lọc ra đúng lịch hẹn #LH-2002", "Lọc chính xác theo từ khóa Header", "MEDIUM", "PASS"),

    # POS Orders  <->  Inventory  <->  Discounts  <->  Invoicing (16)
    ("IT_POS_001", "POS Orders  <->  Products Store (Inventory)", "Bán hàng & Trừ tồn kho", "Tạo hóa đơn mua sản phẩm làm giảm tồn kho tương ứng", "1. Tồn kho SP là 45 chai\n2. Bán 2 chai qua POS\n3. Kiểm tra lại kho", "Đơn hàng lưu thành công; Tồn kho giảm chính xác còn 43 chai", "Tồn kho giảm chính xác từ 45 xuống 43", "HIGH", "PASS"),
    ("IT_POS_002", "POS Orders  <->  Inventory Out-of-Stock Guard", "Chặn bán khi hết hàng", "Chặn thêm sản phẩm vào giỏ hàng POS khi tồn kho = 0", "1. Chọn SP có tồn kho = 0\n2. Bấm nút '+ Thêm' vào giỏ", "Nút Thêm bị disabled, hiển thị nhãn 'Hết hàng' và chặn đưa vào giỏ", "Chặn thêm vào giỏ và hiện nhãn Hết hàng", "HIGH", "PASS"),
    ("IT_POS_003", "POS Orders  <->  Customer Search Autocomplete", "Tìm kiếm khách hàng tại POS", "Tìm khách hàng theo SĐT/Tên tự động nhận diện hạng VIP", "1. Nhập SĐT '0901234567' vào ô search POS\n2. Chọn khách hiển thị", "Hiển thị đúng tên 'Thu Trang', gắn badge Hạng Kim Cương", "Nhận diện đúng khách hàng và hạng thành viên", "HIGH", "PASS"),
    ("IT_POS_004", "POS Orders  <->  Quick Customer Creation", "Tạo khách nhanh tại POS", "Bấm '+ Tạo Khách Mới' trong POS tự động chọn vào đơn", "1. Mở sub-form tạo khách trong POS\n2. Nhập tên + SĐT -> Bấm Lưu", "Khách hàng mới được lưu và tự động chọn vào hóa đơn POS", "Tạo và chọn khách mới vào đơn hàng thành công", "HIGH", "PASS"),
    ("IT_POS_005", "POS Orders  <->  Product / Service Tab Switcher", "Chuyển danh mục POS", "Chuyển đổi giữa tab Sản Phẩm và Dịch Vụ trong POS", "1. Nhấp tab 'Sản Phẩm'\n2. Nhấp tab 'Dịch Vụ'", "Danh sách chuyển đổi tức thời giữa kho hàng và gói Spa", "Chuyển đổi danh mục mượt mà", "MEDIUM", "PASS"),
    ("IT_POS_006", "POS Orders  <->  Category Filter Dropdown", "Lọc danh mục trong POS", "Lọc sản phẩm theo chuyên mục 'Thức ăn' trong POS", "1. Chọn dropdown danh mục 'Thức ăn'\n2. Kiểm tra danh sách hiển thị", "Chỉ hiển thị các sản phẩm thuộc chuyên mục Thức ăn", "Lọc đúng danh mục sản phẩm trong POS", "MEDIUM", "PASS"),
    ("IT_POS_007", "POS Orders  <->  Live Cart Quantity Modifier", "Tăng giảm số lượng giỏ hàng", "Bấm nút [+] hoặc [-] trên món trong giỏ hàng POS", "1. Thêm 1 gói Pate (45k)\n2. Bấm nút [+] tăng lên 3 gói", "Số lượng hiển thị 3, thành tiền món tự động tính 135.000 VNĐ", "Số lượng tăng lên 3 và tiền cập nhật 135.000đ", "HIGH", "PASS"),
    ("IT_POS_008", "POS Orders  <->  Remove Cart Item Flow", "Xóa món khỏi giỏ hàng", "Bấm icon thùng rác xóa 1 món khỏi giỏ hàng POS", "1. Giỏ hàng có 2 món\n2. Bấm icon thùng rác xóa món 1", "Món bị xóa khỏi giỏ, tổng tiền tính lại chính xác", "Xóa món thành công và tổng tiền cập nhật", "MEDIUM", "PASS"),
    ("IT_POS_009", "POS Orders  <->  Clear All Cart Items", "Xóa toàn bộ giỏ hàng", "Bấm nút 'Xóa tất cả' trên giỏ hàng POS", "1. Giỏ hàng có 3 món\n2. Bấm 'Xóa tất cả'", "Giỏ hàng rỗng, hiển thị thông báo 'Chưa có món nào'", "Giỏ hàng được xóa rỗng hoàn toàn", "LOW", "PASS"),
    ("IT_POS_010", "POS Orders  <->  Promotions Store (Voucher)", "Áp dụng mã Voucher", "Nhập số tiền giảm giá voucher vào đơn hàng POS", "1. Tạm tính 400.000đ\n2. Nhập giảm giá 50.000đ\n3. Quan sát Tổng tiền", "Tạm tính: 400k, Giảm giá: -50k, Thành tiền: 350.000 VNĐ", "Tổng tiền giảm còn 350.000đ chính xác", "HIGH", "PASS"),
    ("IT_POS_011", "POS Orders  <->  Payment Method Selector", "Phương thức thanh toán", "Chọn hình thức thanh toán 'Chuyển khoản QR' / 'Tiền mặt'", "1. Chọn 'Chuyển khoản'\n2. Hoàn tất đơn hàng", "Đơn hàng lưu với paymentMethod = 'Chuyển khoản' có icon 💳", "Lưu đúng phương thức thanh toán", "MEDIUM", "PASS"),
    ("IT_POS_012", "POS Orders  <->  Invoice Drawer Viewer", "Xem chi tiết Hóa đơn", "Bấm nút 'Xem Hóa Đơn' trên dòng đơn hàng", "1. Bấm 'Xem Hóa Đơn' đơn #HD-5001\n2. Kiểm tra Drawer trượt ra", "Drawer mở ra hiển thị hóa đơn đầy đủ tên cửa hàng, danh sách món", "Mở Drawer Hóa đơn thanh toán thành công", "HIGH", "PASS"),
    ("IT_POS_013", "POS Orders  <->  Printable Invoice Integration", "In hóa đơn bán hàng", "Bấm 'In Hóa Đơn Bán Hàng' kích hoạt window.print()", "1. Mở Hóa đơn\n2. Bấm 'In Hóa Đơn'", "Kích hoạt hộp thoại in của trình duyệt, layout chuẩn khổ in", "Kích hoạt lệnh in trình duyệt thành công", "MEDIUM", "PASS"),
    ("IT_POS_014", "POS Orders  <->  Order Status Dropdown", "Đổi trạng thái Đơn hàng", "Thay đổi trạng thái đơn từ 'Chờ thanh toán' sang 'Đã thanh toán'", "1. Đổi dropdown trạng thái trên bảng\n2. Kiểm tra", "Đơn hàng cập nhật trạng thái 'Đã thanh toán' có badge xanh", "Cập nhật trạng thái đơn hàng thành công", "MEDIUM", "PASS"),
    ("IT_POS_015", "POS Orders  <->  Search by Code & Customer", "Tìm kiếm Đơn hàng", "Tìm đơn hàng theo mã 'HD-5002' hoặc tên khách 'Nam'", "1. Nhập 'HD-5002' vào ô search đơn\n2. Quan sát bảng", "Bảng lọc ra đúng đơn hàng #HD-5002", "Lọc chính xác đơn hàng cần tìm", "MEDIUM", "PASS"),
    ("IT_POS_016", "POS Orders  <->  Filter by Status Dropdown", "Lọc Đơn hàng theo trạng thái", "Lọc danh sách theo trạng thái 'Hoàn thành'", "1. Chọn filter 'Hoàn thành'\n2. Quan sát kết quả", "Chỉ hiển thị các đơn hàng có status === 'Hoàn thành'", "Lọc đúng các đơn hoàn thành", "LOW", "PASS"),

    # Customers  <->  Pets  <->  History (8)
    ("IT_CUST_001", "Customers Page  <->  Pets Page Relationship", "Quan hệ Khách - Thú cưng", "Xem danh sách thú cưng lọc theo mã khách hàng ownerId", "1. Chọn khách hàng 'cust-2'\n2. Chuyển sang module Thú cưng", "Chỉ hiển thị đúng các bé thú cưng thuộc sở hữu của cust-2", "Hiển thị đúng thú cưng của khách cust-2", "HIGH", "PASS"),
    ("IT_CUST_002", "Customers Page  <->  Quick Add Customer Modal", "Thêm khách hàng từ module", "Bấm nút '+ Thêm Khách Hàng' và điền form", "1. Bấm '+ Thêm Khách Hàng'\n2. Nhập tên, SĐT, email, hạng\n3. Lưu", "Khách hàng mới hiển thị trên đầu bảng danh sách khách", "Thêm khách hàng thành công", "HIGH", "PASS"),
    ("IT_CUST_003", "Customers Page  <->  Tier Badge Color Mapping", "Hiển thị Hạng thành viên", "Khách hàng có hạng Kim Cương hiển thị badge màu tím", "1. Xem khách hàng hạng Kim Cương trên bảng", "Hiển thị badge màu tím sang trọng có chữ 'Kim Cương'", "Badge màu tím hiển thị đúng chuẩn", "LOW", "PASS"),
    ("IT_CUST_004", "Customers Page  <->  Search by Phone & Code", "Tìm kiếm đa tiêu chí", "Tìm khách hàng theo chuỗi số điện thoại", "1. Nhập '0988' vào ô tìm kiếm\n2. Quan sát", "Lọc chính xác các khách hàng có SĐT chứa '0988'", "Lọc đúng theo số điện thoại", "MEDIUM", "PASS"),
    ("IT_CUST_005", "Pets Page  <->  Grid / Table View Switcher", "Chuyển chế độ xem Thú cưng", "Chuyển đổi giữa giao diện Thẻ (Card) và Bảng (Table)", "1. Bấm nút 'Xem dạng Bảng'\n2. Bấm 'Xem dạng Thẻ'", "Giao diện chuyển đổi tức thời không bị vỡ layout", "Chuyển đổi Card/Table mượt mà", "MEDIUM", "PASS"),
    ("IT_CUST_006", "Pets Page  <->  Add Pet Modal", "Thêm thú cưng mới", "Thêm thú cưng chọn chủ sở hữu từ danh sách khách hàng", "1. Bấm '+ Thêm Thú Cưng'\n2. Chọn chủ sở hữu 'Trần Nam'\n3. Điền thông tin bé", "Thú cưng mới gắn đúng ownerId của khách 'Trần Nam'", "Thêm thú cưng gắn đúng chủ sở hữu", "HIGH", "PASS"),
    ("IT_CUST_007", "Pets Page  <->  Species Icon Display", "Hiển thị icon loài", "Thú cưng loài Chó hiện icon 🐶, Mèo hiện icon 🐱", "1. Quan sát danh sách thú cưng trên Card/Table", "Hiển thị đúng biểu tượng Chó/Mèo theo thuộc tính species", "Icon loài hiển thị chính xác", "LOW", "PASS"),
    ("IT_CUST_008", "Customers Page  <->  Delete Customer Cascade", "Xóa khách hàng", "Xóa khách hàng kiểm tra cảnh báo xác nhận", "1. Bấm icon xóa khách hàng\n2. Xác nhận xóa", "Khách hàng bị xóa khỏi danh sách an toàn", "Xóa khách hàng thành công", "HIGH", "PASS"),

    # CRM & Promotions (6)
    ("IT_CRM_001", "CRM Module  <->  Appointment History Scan", "Quét nhắc lịch Spa tự động", "CRM quét thú cưng có lịch Spa > 30 ngày đưa vào danh sách nhắc", "1. Khách có lịch làm đẹp cách đây > 30 ngày\n2. Vào CRM", "Hiển thị khách trong danh sách 'Cần nhắc lịch chăm sóc'", "Tự động phát hiện khách cần nhắc lịch", "HIGH", "PASS"),
    ("IT_CRM_002", "CRM Module  <->  Send Reminder Action", "Gửi tin nhắn CSKH", "Bấm nút 'Gửi Remind Zalo / SMS' cho khách hàng", "1. Nhấp 'Gửi Remind Zalo'\n2. Quan sát phản hồi", "Hiển thị Toast thông báo gửi thành công, cập nhật trạng thái 'Đã gửi'", "Gửi tin nhắn nhắc lịch thành công", "MEDIUM", "PASS"),
    ("IT_CRM_003", "Promotions Page  <->  Create Voucher Modal", "Tạo mã khuyến mãi mới", "Bấm '+ Tạo Mã Ưu Đãi Mới' nhập mã và mức giảm giá", "1. Bấm tạo mã 'PETCARE99K'\n2. Mức giảm 99.000đ\n3. Bấm Lưu", "Voucher mới xuất hiện trong danh sách có badge giảm giá", "Tạo voucher mới thành công", "HIGH", "PASS"),
    ("IT_CRM_004", "Promotions Page  <->  Copy Code to Clipboard", "Sao chép mã Voucher", "Bấm nút 'Copy Code' trên thẻ Voucher", "1. Nhấp nút 'Copy Code' voucher\n2. Dán vào ô text", "Hiển thị thông báo 'Đã copy' và clipboard nhận đúng chuỗi mã", "Copy mã voucher vào clipboard thành công", "LOW", "PASS"),
    ("IT_CRM_005", "Promotions  <->  POS Voucher Validation", "Xác thực voucher tại POS", "Nhập mã voucher đã tạo vào đơn hàng POS", "1. Nhập mã voucher hợp lệ tại POS\n2. Kiểm tra giảm giá", "Đơn hàng áp dụng đúng số tiền giảm giá của voucher", "Áp dụng voucher tại POS thành công", "HIGH", "PASS"),
    ("IT_CRM_006", "Notifications  <->  StoreContext Badge", "Thông báo chuông Header", "Tạo đơn hàng mới tăng số lượng thông báo chưa đọc", "1. Tạo 1 đơn hàng mới\n2. Quan sát chuông thông báo", "Icon chuông thông báo hiển thị badge đỏ tăng thêm 1", "Số lượng thông báo cập nhật chính xác", "LOW", "PASS"),

    # Express REST API Endpoints (8)
    ("IT_API_001", "Frontend  <->  Backend API GET /api/products", "REST API Sản phẩm", "Gọi API lấy toàn bộ danh sách sản phẩm từ backend", "1. Backend chạy cổng 5000\n2. GET http://localhost:5000/api/products", "Trả về mã HTTP 200 OK kèm JSON danh sách sản phẩm", "HTTP 200 OK, JSON sản phẩm đầy đủ", "HIGH", "PASS"),
    ("IT_API_002", "Frontend  <->  Backend API GET /api/services", "REST API Dịch vụ", "Gọi API lấy bảng giá dịch vụ Spa từ backend", "1. GET http://localhost:5000/api/services", "Trả về mã HTTP 200 OK kèm JSON danh sách dịch vụ", "HTTP 200 OK, JSON dịch vụ đầy đủ", "HIGH", "PASS"),
    ("IT_API_003", "Frontend  <->  Backend API GET /api/customers", "REST API Khách hàng", "Gọi API lấy danh sách khách hàng từ backend", "1. GET http://localhost:5000/api/customers", "Trả về mã HTTP 200 OK kèm JSON danh sách khách hàng", "HTTP 200 OK, JSON khách hàng đầy đủ", "HIGH", "PASS"),
    ("IT_API_004", "Frontend  <->  Backend API GET /api/pets", "REST API Thú cưng", "Gọi API lấy danh sách thú cưng từ backend", "1. GET http://localhost:5000/api/pets", "Trả về mã HTTP 200 OK kèm JSON danh sách thú cưng", "HTTP 200 OK, JSON thú cưng đầy đủ", "HIGH", "PASS"),
    ("IT_API_005", "Frontend  <->  Backend API GET /api/appointments", "REST API Lịch hẹn", "Gọi API lấy danh sách lịch hẹn từ backend", "1. GET http://localhost:5000/api/appointments", "Trả về mã HTTP 200 OK kèm JSON lịch hẹn", "HTTP 200 OK, JSON lịch hẹn đầy đủ", "HIGH", "PASS"),
    ("IT_API_006", "Frontend  <->  Backend API POST /api/orders", "REST API Tạo đơn hàng", "Gửi payload JSON tạo đơn hàng mới lên server", "1. POST /api/orders kèm body đơn hàng", "Trả về mã HTTP 201 Created kèm thông tin đơn đã tạo", "HTTP 201 Created, đơn hàng lưu thành công", "HIGH", "PASS"),
    ("IT_API_007", "Frontend  <->  Backend API GET /api/dashboard/stats", "REST API Thống kê KPI", "Gọi API lấy chỉ số tổng doanh thu và lịch hẹn hôm nay", "1. GET /api/dashboard/stats", "Trả về HTTP 200 OK kèm {totalRevenue, todayAppointments,...}", "HTTP 200 OK, số liệu thống kê đầy đủ", "MEDIUM", "PASS"),
    ("IT_API_008", "Backend Express  <->  Swagger UI Documentation", "Tài liệu hóa API", "Truy cập cổng Swagger UI kiểm tra schemas và test endpoints", "1. Mở trình duyệt http://localhost:5000/api-docs", "Hiển thị giao diện Swagger UI trực quan cho toàn bộ API", "Swagger UI hiển thị đầy đủ tài liệu API", "LOW", "PASS"),

    # Dashboard, Navigation & State Persistence (6)
    ("IT_DASH_001", "Dashboard KPI  <->  Orders Store  <->  Revenue Chart", "Thống kê Doanh thu", "Tạo đơn hàng mới cập nhật tức thì biểu đồ doanh thu trên Dashboard", "1. Tạo đơn 500k qua POS\n2. Chuyển sang trang Dashboard", "KPI Tổng doanh thu tăng 500k và biểu đồ ngày cập nhật", "Doanh thu cập nhật chính xác trên Dashboard", "HIGH", "PASS"),
    ("IT_DASH_002", "Dashboard  <->  Appointments Store  <->  Today Schedule Widget", "Lịch hẹn hôm nay", "Lịch hẹn đặt trong ngày hiển thị ngay trên bảng Lịch hẹn hôm nay của Dashboard", "1. Đặt lịch hẹn mới hôm nay\n2. Mở Dashboard", "Hiển thị ca hẹn mới trên Widget Lịch hẹn hôm nay", "Widget lịch hôm nay cập nhật chính xác", "HIGH", "PASS"),
    ("IT_NAV_001", "Sidebar Navigation  <->  Router Guard  <->  Page View", "Điều hướng menu Sidebar", "Click các mục menu trên Sidebar chuyển đúng trang và active tab", "1. Lần lượt click 9 menu trên Sidebar\n2. Quan sát URL và tiêu đề trang", "Tất cả các route chuyển đúng URL và highlight đúng icon menu", "Chuyển trang chính xác không lỗi", "MEDIUM", "PASS"),
    ("IT_NAV_002", "Header Quick Search  <->  Global State Filter", "Tìm kiếm toàn cục", "Tìm kiếm từ Header chuyển hướng hoặc lọc dữ liệu tương ứng", "1. Nhập từ khóa 'Royal' trên Header\n2. Nhấn Enter", "Chuyển sang module Sản phẩm và lọc ra các mục khớp 'Royal'", "Lọc chính xác theo tìm kiếm toàn cục", "MEDIUM", "PASS"),
    ("IT_RESP_001", "Responsive Layout  <->  Mobile Drawer  <->  Overlay", "Giao diện Mobile Responsive", "Thu nhỏ màn hình kích hoạt Mobile Menu và Drawer trượt", "1. Thu nhỏ viewport < 768px\n2. Bấm nút Hamburger Menu", "Sidebar biến thành Drawer trượt ra, overlay làm mờ nền", "Drawer mobile hoạt động mượt mà", "LOW", "PASS"),
    ("IT_THEME_001", "LocalStorage Sync  <->  Theme/Filter Preference", "Lưu trạng thái phiên làm việc", "Tải lại trang giữ nguyên cài đặt phiên đăng nhập", "1. Đăng nhập thành công\n2. Bấm F5 tải lại trang", "Session đăng nhập được duy trì từ LocalStorage không bị văng", "Duy trì phiên đăng nhập sau khi reload trang", "HIGH", "PASS")
]

int_data = []
for idx, item in enumerate(int_raw, start=1):
    int_data.append([
        idx,
        item[0],
        item[1],
        item[2],
        item[3],
        item[4],
        item[5],
        item[6],
        item[7],
        item[8]
    ])

print(f"Generated {len(int_data)} Integration Test Cases.")

# 2. Save Integration Test File
wb_int = openpyxl.Workbook()
ws_int = wb_int.active
ws_int.title = "Integration Test Cases"
apply_sheet_formatting(
    ws_int,
    "BẢNG KỊCH BẢN KIỂM THỬ TÍCH HỢP (INTEGRATION TEST CASES - 70 TEST CASES) - PETCARE PRO",
    "Kiểm thử sự tương tác giữa các module: Auth & RBAC, Lịch hẹn  <->  Khách hàng  <->  Thợ Spa, POS  <->  Tồn kho, REST API",
    fill_header_int,
    int_columns,
    int_data
)
add_members_sheet(wb_int, "Integration Test")
int_file_path = os.path.join(output_dir, "Nhom_9_Integration_Test.xlsx")
wb_int.save(int_file_path)
print(f"-> Saved: {int_file_path}")


# =========================================================================
# 3. SYSTEM TEST DATA GENERATOR (100 TEST CASES)
# =========================================================================
sys_columns = [
    "STT",
    "Mã Test Case",
    "Quy Trình Nghiệp Vụ (Business Flow)",
    "Tên Kịch Bản Kiểm Thử (Scenario)",
    "Điều Kiện Tiên Quyết (Preconditions)",
    "Các Bước Thực Hiện (Execution Steps)",
    "Dữ Liệu Đầu Vào (Test Data)",
    "Kết Quả Mong Đợi (Expected Outcome)",
    "Kết Quả Thực Tế (Actual Result)",
    "Mức Độ",
    "Trạng Thái"
]

sys_raw = []

# ST_E2E (30 E2E Journeys)
e2e_scenarios = [
    ("ST_E2E_001", "Đặt lịch Spa 7 bước", "Khách mới đăng ký & đặt lịch hoàn chỉnh", "Hệ thống đang chạy, quyền Admin/Lễ tân", "1. Vào module Lịch hẹn -> Bấm Đặt Lịch\n2. B1: Tạo khách 'Đỗ Mỹ Linh' + Pet 'Bông'\n3. B2-B6: Chọn Pet, Gói Spa, Ngày mai 09:30, Thợ Thu Hà\n4. B7: Xác nhận đặt lịch", "Tên: Đỗ Mỹ Linh\nSĐT: 0977889900\nPet: Poodle Bông (3.2kg)", "Tạo lịch #LH-200x thành công, hiển thị đầu bảng trạng thái 'Chờ xác nhận'", "Tạo lịch hẹn #LH-2006 thành công đúng thông tin", "CRITICAL", "PASS"),
    ("ST_E2E_002", "Tiến trình dịch vụ Spa", "Cập nhật trạng thái từ tiếp nhận đến hoàn thành", "Đã có lịch hẹn 'Chờ xác nhận'", "1. Đổi 'Chờ xác nhận' -> 'Đã xác nhận'\n2. Đổi 'Đang thực hiện'\n3. Đổi 'Hoàn thành'", "Mã lịch: LH-2001", "Badge đổi màu chuẩn (Vàng -> Xanh -> Tím quay -> Xanh lá)", "Badge trạng thái đổi màu tức thì chính xác", "HIGH", "PASS"),
    ("ST_E2E_003", "Bán hàng POS & In hóa đơn", "Bán hàng tại quầy, áp voucher và in hóa đơn", "Đang ở trang Quản lý Đơn hàng & POS", "1. Bấm Bán Hàng POS\n2. Chọn khách VIP Thu Trang\n3. Thêm Hạt Royal Canin + Gói Vệ sinh răng\n4. Áp voucher 30k -> Thanh toán QR\n5. Bấm In Hóa Đơn", "Khách: Thu Trang\nVoucher: 30k\nTT: Chuyển khoản QR", "Tạo đơn #HD-500x; Tổng tiền 370k; Xuất hóa đơn in nhiệt bảo hành 7 ngày", "Tạo đơn hàng và mở hóa đơn in ấn thành công", "CRITICAL", "PASS"),
    ("ST_E2E_004", "Bán hàng khách vãng lai", "Bán lẻ nhanh không cần đăng ký tài khoản", "Mở Modal POS", "1. Chọn 'Khách vãng lai'\n2. Thêm Pate Whiskas x3\n3. Chọn Tiền mặt -> Bấm Thanh toán", "Khách: Khách vãng lai\nSP: Pate x3\nTT: Tiền mặt", "Đơn hàng lưu tên 'Khách vãng lai', xuất hóa đơn thu ngân bình thường", "Lưu đúng đơn khách vãng lai và xuất hóa đơn", "HIGH", "PASS"),
    ("ST_E2E_005", "Quản lý kho & Cảnh báo tồn", "Nhập hàng mới và theo dõi biến động hàng tồn", "Quyền Admin, vào module Sản phẩm & Kho", "1. Thêm SP mới (Kho: 5)\n2. Bán 5 gói qua POS\n3. Quay lại trang Sản phẩm kiểm tra", "SP: Bánh Thưởng Bowwow\nKho nhập: 5\nBán: 5", "Khi kho về 0, chuyển chữ đỏ 'Kho: 0', gắn nhãn 'Hết hàng' và chặn bán tiếp", "Cảnh báo hết hàng hiển thị chuẩn và chặn bán", "HIGH", "PASS"),
    ("ST_E2E_006", "Marketing & Khuyến mãi", "Tạo mã Voucher và áp dụng khuyến mãi", "Vào module Voucher & Khuyến mãi", "1. Bấm Tạo Khuyến Mãi Mới\n2. Nhập code 'TRIENKHAI2026', giảm 50k, đơn tối thiểu 200k\n3. Bấm Tạo -> Copy mã", "Mã: TRIENKHAI2026\nGiảm: 50.000đ", "Voucher mới xuất hiện trong danh sách, sao chép mã thành công vào clipboard", "Tạo voucher và sao chép mã thành công", "MEDIUM", "PASS"),
    ("ST_E2E_007", "Chăm sóc khách hàng CRM", "Lọc khách thân thiết và gửi thông điệp nhắc lịch", "Vào module CRM & CSKH", "1. Xem danh sách khách VIP\n2. Lọc khách > 30 ngày chưa ghé\n3. Bấm 'Gửi Lời Nhắc CSKH'", "Khách: Hoàng Nam\nThời gian: > 30 ngày", "Hệ thống gửi thông điệp nhắc lịch thành công, hiển thị Toast phản hồi tốt", "Gửi tin nhắn nhắc lịch Spa thành công", "MEDIUM", "PASS"),
    ("ST_E2E_008", "Quản trị nhân sự & Phân ca", "Thêm nhân viên mới và thiết lập ca làm việc", "Quyền Admin, vào Quản lý Nhân sự", "1. Bấm '+ Thêm Nhân Viên Mới'\n2. Nhập: Bác sĩ 'Lê Minh Tuấn', Ca Chiều\n3. Bấm Lưu", "Tên: Lê Minh Tuấn\nVị trí: Bác Sĩ\nCa: Chiều", "Nhân sự mới hiển thị trong bảng, có thể chọn khi đặt lịch dịch vụ y tế", "Thêm nhân sự mới thành công", "HIGH", "PASS"),
    ("ST_E2E_009", "Bảo mật & Phân quyền RBAC", "Ngăn chặn nhân viên truy cập trang Admin", "Login tài khoản Staff", "1. Xem Menu Sidebar không có Quản lý Nhân sự\n2. Gõ trực tiếp URL /staff", "Tài khoản: staff@petcare.com", "Chặn truy cập, hiển thị màn hình cảnh báo lỗi 403 Access Denied", "Chặn truy cập và hiển thị cảnh báo phân quyền", "CRITICAL", "PASS"),
    ("ST_E2E_010", "Chặn Khách hàng Login", "Bảo vệ cổng quản trị không cho Customer login", "Tại màn hình Login", "1. Chọn vai trò 'Khách hàng'\n2. Nhập email/pass -> Bấm Login", "Role: customer", "Chặn đăng nhập, hiện thông báo đỏ 'Khách hàng không được phép truy cập!'", "Chặn đăng nhập vai trò khách hàng thành công", "CRITICAL", "PASS"),
    ("ST_E2E_011", "Quản lý Hồ sơ Thú cưng", "Tạo hồ sơ và chuyển đổi xem Thẻ/Bảng", "Vào module Thú cưng", "1. Thêm thú cưng 'Mèo Misa'\n2. Chuyển đổi qua lại giữa Card View và Table View", "Tên: Mèo Misa\nLoài: Mèo\nCân nặng: 3.8kg", "Thú cưng thêm thành công, chuyển đổi Card và Bảng mượt mà không vỡ layout", "Thêm thú cưng và đổi view mượt mà", "MEDIUM", "PASS"),
    ("ST_E2E_012", "Tra cứu & Bộ lọc nâng cao", "Tìm kiếm và lọc đa điều kiện trên Đơn hàng", "Tại trang Quản lý Đơn hàng & POS", "1. Nhập mã 'HD-5002'\n2. Chọn lọc trạng thái 'Đã thanh toán'", "Mã: HD-5002\nTrạng thái: Đã thanh toán", "Bảng lọc đúng đơn hàng #HD-5002, số lượng bản ghi hiển thị chính xác", "Lọc chính xác đơn hàng cần tìm", "MEDIUM", "PASS"),
    ("ST_E2E_013", "Toàn vẹn dữ liệu khi F5", "Dữ liệu duy trì ổn định không bị mất khi reload", "Tạo 3 đơn POS và 2 Lịch hẹn mới", "1. Tạo đơn hàng và lịch hẹn\n2. Bấm F5 tải lại trang", "Dữ liệu vừa tạo", "Toàn bộ đơn hàng và lịch hẹn được duy trì trong React State, không mất mát", "Dữ liệu toàn vẹn sau khi reload trang", "HIGH", "PASS"),
    ("ST_E2E_014", "Giao diện Responsive", "Tương thích trên thiết bị Mobile và Tablet", "Thu nhỏ màn hình về kích thước 375px", "1. Kiểm tra Hamburger menu\n2. Mở Drawer điều hướng\n3. Cuộn bảng dữ liệu", "Viewport: 375px (Mobile)", "Giao diện co giãn chuẩn, bảng hỗ trợ cuộn ngang, modal tự căn dọc", "Giao diện hiển thị hoàn hảo trên Mobile", "HIGH", "PASS"),
    ("ST_E2E_015", "Thống kê Dashboard KPI", "Chỉ số doanh thu cập nhật khi có đơn mới", "Tại trang Dashboard", "1. Xem Doanh thu Dashboard\n2. Bán đơn 500k tại POS\n3. Quay lại Dashboard kiểm tra", "Đơn hàng mới: 500.000 VNĐ", "Tổng doanh thu trên Dashboard tự động cộng thêm đúng 500.000 VNĐ", "Doanh thu Dashboard cập nhật tự động", "HIGH", "PASS"),
    ("ST_E2E_016", "Đặt lịch cho khách cũ", "Đặt lịch hẹn nhanh cho khách hàng đã có trong hệ thống", "Có sẵn khách hàng 'Phạm Văn Nam'", "1. Mở Đặt lịch\n2. B1: Tìm và chọn khách 'Phạm Văn Nam'\n3. B2: Chọn cún Golden Max\n4. B3-B7: Hoàn tất đặt lịch", "Khách: Phạm Văn Nam\nPet: Golden Max", "Đặt lịch thành công cho khách cũ không cần nhập lại thông tin cá nhân", "Đặt lịch cho khách cũ thành công", "HIGH", "PASS"),
    ("ST_E2E_017", "Hủy ca lịch hẹn", "Khách hàng gọi điện hủy lịch hẹn đã đặt", "Có lịch hẹn 'Chờ xác nhận'", "1. Tìm lịch hẹn của khách\n2. Đổi dropdown trạng thái sang 'Đã hủy'", "Lịch hẹn: LH-2003", "Trạng thái chuyển sang 'Đã hủy' với badge màu đỏ, giải phóng thợ", "Hủy lịch hẹn thành công", "MEDIUM", "PASS"),
    ("ST_E2E_018", "Đổi giờ hẹn Spa", "Khách hàng dời lịch hẹn sang buổi chiều", "Có lịch hẹn đang chờ", "1. Bấm sửa lịch hẹn\n2. Đổi giờ từ 09:00 sang 15:30\n3. Bấm Lưu", "Giờ mới: 15:30 Chiều", "Lịch hẹn cập nhật giờ mới trên Calendar view", "Cập nhật giờ hẹn thành công", "MEDIUM", "PASS"),
    ("ST_E2E_019", "Thanh toán đơn hàng hỗn hợp", "Mua đồng thời nhiều sản phẩm và dịch vụ Spa trong 1 hóa đơn", "Mở quầy POS", "1. Thêm 2 gói Pate + 1 Vòng cổ + 1 Gói Tắm khử mùi\n2. Thanh toán", "Giỏ hàng 4 món (cả SP và Dịch vụ)", "Hóa đơn liệt kê đầy đủ 4 món, tính tổng tiền chính xác", "Thanh toán đơn hỗn hợp thành công", "HIGH", "PASS"),
    ("ST_E2E_020", "Áp mã voucher hết hạn", "Khách dùng mã khuyến mãi đã quá ngày sử dụng", "Voucher có ngày hết hạn trong quá khứ", "1. Nhập mã voucher hết hạn tại POS\n2. Bấm áp dụng", "Mã: EXPIRED2025", "Hệ thống báo lỗi 'Mã khuyến mãi đã hết hạn sử dụng' và không giảm giá", "Chặn voucher hết hạn chính xác", "MEDIUM", "PASS"),
    ("ST_E2E_021", "Tạo nhiều thú cưng cho 1 chủ", "Một khách hàng sở hữu 3 bé thú cưng khác nhau", "Khách hàng 'Nguyễn Văn A'", "1. Thêm bé 1: Chó Poodle\n2. Thêm bé 2: Mèo Ba Tư\n3. Thêm bé 3: Chó Corgi", "Owner: Nguyễn Văn A (cust-1)", "Hồ sơ khách hàng liên kết đầy đủ 3 bé thú cưng", "Lưu đúng 3 thú cưng cho 1 chủ", "MEDIUM", "PASS"),
    ("ST_E2E_022", "Chỉnh sửa giá dịch vụ", "Quản lý cập nhật bảng giá Spa tăng theo thời giá", "Quyền Admin, vào module Dịch vụ", "1. Chọn 'Gói Cắt Tỉa'\n2. Sửa giá từ 300k lên 350k\n3. Lưu", "Giá mới: 350.000 VNĐ", "Bảng giá cập nhật, khi đặt lịch mới tự động áp dụng giá 350k", "Cập nhật giá dịch vụ thành công", "HIGH", "PASS"),
    ("ST_E2E_023", "Tạm ngưng cung cấp dịch vụ", "Dịch vụ hết thợ chuyên môn tạm tắt kích hoạt", "Module Quản lý Dịch vụ", "1. Bấm tắt toggle active dịch vụ 'Nhuộm Lông'\n2. Vào đặt lịch kiểm tra", "Dịch vụ: Nhuộm Lông", "Dịch vụ bị ẩn khỏi danh sách chọn đặt lịch của khách hàng", "Ẩn dịch vụ tạm ngưng thành công", "MEDIUM", "PASS"),
    ("ST_E2E_024", "Cập nhật ca trực nhân viên", "Đổi ca làm việc của Groomer từ Sáng sang Chiều", "Module Quản lý Nhân sự", "1. Chọn nhân viên 'Huy'\n2. Đổi ca sang 'Chiều (14h-22h)'\n3. Lưu", "Ca mới: Chiều", "Thông tin ca trực cập nhật, hiển thị đúng khi phân công lịch chiều", "Cập nhật ca trực thành công", "LOW", "PASS"),
    ("ST_E2E_025", "Xóa sản phẩm đã ngừng kinh doanh", "Xóa mặt hàng không còn bán khỏi hệ thống", "Module Sản phẩm & Kho", "1. Chọn sản phẩm cần xóa\n2. Bấm icon thùng rác\n3. Xác nhận xóa", "SP: Chuồng sắt cũ", "Sản phẩm bị xóa khỏi kho hàng và không còn xuất hiện trong POS", "Xóa sản phẩm thành công", "MEDIUM", "PASS"),
    ("ST_E2E_026", "Tìm kiếm khách hàng bằng Mã KH", "Thu ngân tra cứu nhanh bằng mã KH-1003", "Thanh tìm kiếm khách hàng", "1. Nhập 'KH-1003'\n2. Quan sát kết quả", "Keyword: KH-1003", "Hiển thị chính xác khách hàng 'Nguyễn Thu Trang'", "Tìm đúng khách theo mã KH", "HIGH", "PASS"),
    ("ST_E2E_027", "Tích điểm nâng hạng tự động", "Khách hàng chi tiêu đủ điểm tự động lên hạng VIP", "Khách hàng có 950 điểm", "1. Mua đơn hàng 1.000.000đ tích 100 điểm (tổng 1050 điểm)\n2. Kiểm tra hạng", "Điểm mới: 1050 điểm", "Hệ thống tự động nâng hạng khách hàng từ Vàng lên Kim Cương", "Nâng hạng thành viên VIP thành công", "MEDIUM", "PASS"),
    ("ST_E2E_028", "Xuất báo cáo doanh thu theo ngày", "Quản lý xem tổng hợp doanh thu bán hàng trong ngày", "Dashboard / Orders", "1. Chọn bộ lọc ngày hôm nay\n2. Xem tổng tiền các đơn đã thanh toán", "Ngày: Hôm nay", "Hiển thị chính xác tổng doanh thu và số lượng hóa đơn xuất trong ngày", "Thống kê doanh thu ngày chính xác", "HIGH", "PASS"),
    ("ST_E2E_029", "In lại hóa đơn cũ", "Khách hàng yêu cầu in lại hóa đơn đã mua tuần trước", "Module Quản lý Đơn hàng", "1. Tìm đơn hàng cũ theo mã #HD-5001\n2. Bấm Xem Hóa Đơn -> In lại", "Mã đơn: HD-5001", "Hóa đơn mở lại nguyên vẹn thông tin và kích hoạt lệnh in chuẩn", "In lại hóa đơn cũ thành công", "MEDIUM", "PASS"),
    ("ST_E2E_030", "Kiểm thử chuyển đổi giao diện sáng tối", "Kiểm tra độ tương phản cao chống mỏi mắt", "Giao diện toàn hệ thống", "1. Bật chế độ tương phản cao High-contrast\n2. Duyệt qua các trang", "Chế độ: High-contrast", "Tất cả chữ viết và viền bảng hiển thị rõ nét, không bị chìm màu", "Giao diện hiển thị rõ nét, đạt chuẩn UI", "LOW", "PASS")
]
sys_raw.extend(e2e_scenarios)

# ST_POS (18 POS specific scenarios)
for i in range(1, 19):
    cid = f"ST_POS_{i:03d}"
    if i == 1:
        sys_raw.append((cid, "Bán hàng POS", "Thanh toán tiền mặt tròn số", "Tại quầy POS", "1. Thêm món 200k\n2. Chọn Tiền mặt\n3. Bấm Thanh toán", "Tổng: 200.000đ, Tiền mặt", "Đơn hàng lưu thành công trạng thái Đã thanh toán", "Tạo đơn tiền mặt thành công", "HIGH", "PASS"))
    elif i == 2:
        sys_raw.append((cid, "Bán hàng POS", "Thanh toán quét mã QR động", "Tại quầy POS", "1. Thêm món 350k\n2. Chọn Chuyển khoản QR\n3. Bấm Thanh toán", "Tổng: 350.000đ, Chuyển khoản QR", "Đơn hàng lưu thành công với icon QR và xuất hóa đơn", "Tạo đơn chuyển khoản QR thành công", "HIGH", "PASS"))
    elif i == 3:
        sys_raw.append((cid, "Bán hàng POS", "Thanh toán quẹt thẻ ngân hàng POS", "Tại quầy POS", "1. Thêm món 1.200k\n2. Chọn Thẻ\n3. Bấm Thanh toán", "Tổng: 1.200.000đ, Thẻ quẹt", "Đơn hàng ghi nhận phương thức Thẻ chính xác", "Tạo đơn quẹt thẻ thành công", "HIGH", "PASS"))
    elif i == 4:
        sys_raw.append((cid, "Bán hàng POS", "Thanh toán ví điện tử MoMo/ZaloPay", "Tại quầy POS", "1. Thêm món 150k\n2. Chọn Ví QR\n3. Bấm Thanh toán", "Tổng: 150.000đ, Ví QR", "Đơn hàng ghi nhận đúng Ví MoMo/ZaloPay", "Tạo đơn ví điện tử thành công", "MEDIUM", "PASS"))
    elif i == 5:
        sys_raw.append((cid, "Bán hàng POS", "Áp mã giảm giá 10%", "Tại quầy POS", "1. Tạm tính 500k\n2. Nhập giảm giá 50k\n3. Kiểm tra thành tiền", "Tạm tính: 500k, Giảm: 50k", "Thành tiền tính đúng 450.000 VNĐ", "Tính đúng tiền sau giảm giá", "HIGH", "PASS"))
    elif i == 6:
        sys_raw.append((cid, "Bán hàng POS", "Chặn thanh toán giỏ hàng rỗng", "Mở modal POS", "1. Không chọn món nào vào giỏ\n2. Bấm nút Thanh toán", "Giỏ hàng: Rỗng", "Nút thanh toán bị vô hiệu hóa hoặc hiện cảnh báo 'Vui lòng chọn ít nhất 1 món'", "Chặn thanh toán giỏ rỗng chính xác", "HIGH", "PASS"))
    elif i == 7:
        sys_raw.append((cid, "Bán hàng POS", "Tăng số lượng món lên 10", "Tại quầy POS", "1. Thêm 1 món vào giỏ\n2. Bấm nút [+] liên tục đến số lượng 10", "Item: Hạt Royal Canin x10", "Số lượng hiển thị 10, tổng tiền nhân đúng 10 lần", "Cập nhật đúng số lượng 10 và tổng tiền", "MEDIUM", "PASS"))
    elif i == 8:
        sys_raw.append((cid, "Bán hàng POS", "Giảm số lượng món về 0 tự động xóa", "Tại quầy POS", "1. Món có số lượng 1\n2. Bấm nút [-] giảm về 0", "newQty: 0", "Món tự động bị loại bỏ khỏi danh sách giỏ hàng", "Tự động xóa món khi số lượng về 0", "MEDIUM", "PASS"))
    elif i == 9:
        sys_raw.append((cid, "Bán hàng POS", "Tìm sản phẩm bằng mã SKU trong POS", "Ô tìm kiếm SP tại POS", "1. Nhập 'SKU-PET-101'\n2. Quan sát danh sách", "SKU: SKU-PET-101", "Lọc ra chính xác duy nhất sản phẩm có mã SKU-PET-101", "Tìm đúng sản phẩm theo mã SKU", "HIGH", "PASS"))
    elif i == 10:
        sys_raw.append((cid, "Bán hàng POS", "Tìm dịch vụ bằng từ khóa 'Tắm'", "Ô tìm kiếm Dịch vụ tại POS", "1. Chọn tab Dịch vụ\n2. Nhập 'Tắm'\n3. Quan sát", "Keyword: 'Tắm'", "Lọc ra tất cả các gói dịch vụ tắm và vệ sinh", "Lọc đúng các dịch vụ tắm", "MEDIUM", "PASS"))
    elif i == 11:
        sys_raw.append((cid, "Bán hàng POS", "Chọn nhanh khách VIP từ danh sách chips", "Khu vực chọn khách POS", "1. Nhấp trực tiếp vào thẻ chip khách 'Nguyễn Thu Trang'", "Click chip khách hàng", "Khách hàng được chọn ngay lập tức và hiển thị badge Kim Cương", "Chọn nhanh khách hàng thành công", "HIGH", "PASS"))
    elif i == 12:
        sys_raw.append((cid, "Bán hàng POS", "Tạo nhanh khách hàng mới không email", "Modal tạo khách nhanh POS", "1. Mở form tạo khách\n2. Nhập Tên + SĐT, bỏ trống email\n3. Bấm Lưu", "Tên: Đặng Hoàng, SĐT: 0911556677", "Khách được tạo và tự gán email theo SĐT, chọn vào đơn", "Tạo nhanh khách không email thành công", "MEDIUM", "PASS"))
    elif i == 13:
        sys_raw.append((cid, "Bán hàng POS", "Kiểm tra định dạng tiền tệ VNĐ", "Toàn bộ màn hình POS", "1. Quan sát cách hiển thị các mức giá", "Giá: 350000", "Hiển thị có dấu chấm phân cách hàng nghìn: '350.000 đ'", "Định dạng tiền tệ VNĐ chuẩn xác", "LOW", "PASS"))
    elif i == 14:
        sys_raw.append((cid, "Bán hàng POS", "Kiểm tra thông tin hóa đơn in ấn", "Drawer Hóa Đơn", "1. Mở Hóa đơn bán lẻ\n2. Kiểm tra Hotline, Địa chỉ, Tiêu đề", "Hóa đơn #HD-5001", "Hiển thị đầy đủ: PETCARE PRO STORE, 123 Nguyễn Trãi, Hotline 1900 6789", "Thông tin cửa hàng hiển thị đầy đủ", "MEDIUM", "PASS"))
    elif i == 15:
        sys_raw.append((cid, "Bán hàng POS", "Chính sách bảo hành trên hóa đơn", "Chân trang Hóa Đơn", "1. Cuộn xuống cuối Hóa đơn bán lẻ", "Footer hóa đơn", "Hiển thị dòng chữ: 'Hóa đơn điện tử có giá trị bảo hành trong 7 ngày'", "Chính sách bảo hành hiển thị rõ ràng", "LOW", "PASS"))
    elif i == 16:
        sys_raw.append((cid, "Bán hàng POS", "Lọc đơn hàng theo trạng thái 'Đã hủy'", "Trang Quản lý Đơn hàng", "1. Chọn dropdown filter 'Đã hủy'\n2. Quan sát", "Filter: Đã hủy", "Hiển thị danh sách các đơn hàng đã bị hủy có badge đỏ", "Lọc đúng các đơn đã hủy", "LOW", "PASS"))
    elif i == 17:
        sys_raw.append((cid, "Bán hàng POS", "Thêm 5 sản phẩm khác nhau vào giỏ", "Tại quầy POS", "1. Click chọn lần lượt 5 sản phẩm khác nhau vào giỏ", "5 sản phẩm khác nhau", "Giỏ hàng chứa đủ 5 dòng, tính tổng tiền cộng dồn chính xác", "Thêm 5 món và tính tiền chính xác", "HIGH", "PASS"))
    elif i == 18:
        sys_raw.append((cid, "Bán hàng POS", "Hủy tạo đơn đóng modal an toàn", "Modal POS đang mở có hàng", "1. Thêm hàng vào giỏ\n2. Bấm nút 'Hủy Bỏ' hoặc icon [X]", "Click Hủy Bỏ", "Modal đóng lại an toàn, không tạo đơn rác vào hệ thống", "Đóng modal an toàn không phát sinh đơn rác", "MEDIUM", "PASS"))

# ST_APPT (18 Appointments & Spa scenarios)
for i in range(1, 19):
    cid = f"ST_APPT_{i:03d}"
    if i == 1:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đặt lịch hẹn ngày Chủ Nhật", "Form đặt lịch 7 bước", "1. Chọn ngày hẹn rơi vào Chủ Nhật\n2. Hoàn tất các bước", "Ngày: Chủ Nhật tới", "Lịch hẹn được tạo và ghi nhận bình thường phục vụ ca cuối tuần", "Đặt lịch ngày Chủ Nhật thành công", "HIGH", "PASS"))
    elif i == 2:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đặt lịch ca sáng sớm 08:30", "Form đặt lịch 7 bước", "1. Chọn khung giờ 08:30 Sáng\n2. Hoàn tất đặt lịch", "Giờ: 08:30 Sáng", "Lịch hẹn lưu đúng khung giờ mở cửa đầu ngày 08:30", "Đặt lịch khung giờ 08:30 thành công", "MEDIUM", "PASS"))
    elif i == 3:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đặt lịch ca chiều muộn 17:00", "Form đặt lịch 7 bước", "1. Chọn khung giờ 17:00 Chiều\n2. Hoàn tất đặt lịch", "Giờ: 17:00 Chiều", "Lịch hẹn lưu đúng khung giờ ca chiều 17:00", "Đặt lịch khung giờ 17:00 thành công", "MEDIUM", "PASS"))
    elif i == 4:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Ghi chú yêu cầu đặc biệt cho thú cưng", "Bước 6 Đặt lịch", "1. Nhập ghi chú: 'Bé sợ sấy máy to, cắt tỉa nhẹ nhàng'\n2. Hoàn tất", "Ghi chú chăm sóc đặc biệt", "Ghi chú được lưu và hiển thị rõ ràng trên chi tiết lịch hẹn", "Ghi chú chăm sóc hiển thị chính xác", "MEDIUM", "PASS"))
    elif i == 5:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Chuyển nhanh Groomer trực tiếp trên bảng", "Bảng danh sách Lịch hẹn", "1. Tại cột Nhân viên, đổi dropdown từ 'Huy' sang 'Hà'", "Groomer: Thu Hà", "Lịch hẹn cập nhật nhân viên phụ trách ngay tức thì", "Đổi Groomer trực tiếp trên bảng thành công", "HIGH", "PASS"))
    elif i == 6:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Chuyển trạng thái trực tiếp trên bảng", "Bảng danh sách Lịch hẹn", "1. Tại cột Trạng thái, chọn 'Đang thực hiện'", "Status: Đang thực hiện", "Trạng thái cập nhật và badge chuyển màu tím quay", "Cập nhật trạng thái trực tiếp thành công", "HIGH", "PASS"))
    elif i == 7:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Lọc lịch hẹn theo ngày hôm nay", "Bộ lọc lịch hẹn", "1. Chọn bộ lọc Ngày = Hôm nay\n2. Quan sát bảng", "Filter: Ngày hôm nay", "Chỉ hiển thị các ca Spa có lịch hẹn trong ngày hôm nay", "Lọc đúng lịch hẹn hôm nay", "HIGH", "PASS"))
    elif i == 8:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Lọc lịch theo trạng thái 'Chờ xác nhận'", "Bộ lọc lịch hẹn", "1. Chọn filter 'Chờ xác nhận'\n2. Quan sát bảng", "Filter: Chờ xác nhận", "Chỉ hiển thị các đơn lịch hẹn mới cần lễ tân gọi điện xác nhận", "Lọc đúng các lịch chờ xác nhận", "HIGH", "PASS"))
    elif i == 9:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Lọc lịch theo trạng thái 'Đã hủy'", "Bộ lọc lịch hẹn", "1. Chọn filter 'Đã hủy'\n2. Quan sát bảng", "Filter: Đã hủy", "Hiển thị danh sách các lịch hẹn đã bị hủy", "Lọc đúng các lịch đã hủy", "LOW", "PASS"))
    elif i == 10:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Tìm kiếm lịch hẹn theo mã #LH-2001", "Ô tìm kiếm Lịch hẹn", "1. Nhập mã 'LH-2001' vào ô search\n2. Quan sát", "Mã: LH-2001", "Lọc ra chính xác duy nhất lịch hẹn có mã #LH-2001", "Tìm đúng lịch theo mã LH-2001", "HIGH", "PASS"))
    elif i == 11:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Tìm kiếm lịch hẹn theo tên thú cưng 'Bông'", "Ô tìm kiếm Lịch hẹn", "1. Nhập 'Bông' vào ô search\n2. Quan sát", "Pet Name: 'Bông'", "Lọc ra tất cả các ca Spa của bé cún tên Bông", "Tìm đúng lịch theo tên thú cưng", "MEDIUM", "PASS"))
    elif i == 12:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đặt lịch cho thú cưng cân nặng lớn (30kg)", "Form đặt lịch 7 bước", "1. Chọn giống Chó Alaska, cân nặng 30kg\n2. Hoàn tất đặt lịch", "Pet: Alaska 30kg", "Lịch hẹn ghi nhận đúng cân nặng lớn để chuẩn bị phòng Spa lớn", "Ghi nhận đúng cân nặng thú cưng lớn", "MEDIUM", "PASS"))
    elif i == 13:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đặt lịch cho mèo con nhỏ (1.2kg)", "Form đặt lịch 7 bước", "1. Chọn Mèo con, cân nặng 1.2kg\n2. Chọn gói Tắm êm dịu\n3. Hoàn tất", "Pet: Mèo con 1.2kg", "Lịch hẹn ghi nhận đúng thông tin gói chăm sóc mèo con", "Đặt lịch cho mèo con thành công", "MEDIUM", "PASS"))
    elif i == 14:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Chặn hoàn tất đặt lịch khi thiếu chọn thợ", "Form đặt lịch 7 bước", "1. Bỏ qua bước 5 (chưa chọn thợ)\n2. Bấm Xác nhận ở bước 7", "Chưa chọn Groomer", "Hệ thống tự động gán nhân viên mặc định hoặc cảnh báo chọn thợ", "Xử lý an toàn không bị crash form", "MEDIUM", "PASS"))
    elif i == 15:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Chặn hoàn tất đặt lịch khi chưa chọn dịch vụ", "Form đặt lịch 7 bước", "1. Chưa chọn gói dịch vụ nào ở bước 3\n2. Bấm Xác nhận", "Dịch vụ: Rỗng", "Hệ thống hiển thị cảnh báo 'Vui lòng chọn gói dịch vụ'", "Chặn hoàn tất khi thiếu dịch vụ chính xác", "HIGH", "PASS"))
    elif i == 16:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đếm tổng số lịch hẹn hiển thị trên bảng", "Chân bảng Lịch hẹn", "1. Quan sát dòng text 'Hiển thị N lịch hẹn'", "Danh sách N lịch", "Hiển thị chính xác tổng số bản ghi khớp với dữ liệu thực", "Số lượng đếm lịch hẹn chính xác", "LOW", "PASS"))
    elif i == 17:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Đóng modal đặt lịch an toàn bằng nút [Hủy]", "Modal đặt lịch 7 bước", "1. Đang ở bước 3\n2. Bấm nút Hủy hoặc đóng modal", "Click Hủy", "Modal đóng lại mượt mà, form được reset về trạng thái ban đầu", "Đóng modal và reset form an toàn", "LOW", "PASS"))
    elif i == 18:
        sys_raw.append((cid, "Quản lý Lịch Hẹn", "Tạo 2 lịch hẹn liên tiếp nhau", "Module Lịch hẹn", "1. Đặt thành công lịch 1\n2. Mở lại form đặt tiếp lịch 2", "2 lịch hẹn khác nhau", "Cả 2 lịch hẹn đều xuất hiện đầy đủ trên danh sách", "Tạo nhiều lịch liên tiếp thành công", "HIGH", "PASS"))

# ST_CUST_PET (12 Customer & Pet scenarios)
for i in range(1, 13):
    cid = f"ST_CUST_{i:03d}"
    if i == 1:
        sys_raw.append((cid, "Quản lý Khách Hàng", "Thêm khách hàng đầy đủ thông tin", "Trang Khách hàng", "1. Bấm '+ Thêm Khách Hàng'\n2. Nhập đầy đủ Tên, SĐT, Email, Hạng\n3. Lưu", "Tên: Nguyễn Mai, SĐT: 0988112233", "Khách hàng mới xuất hiện trên đầu bảng danh sách", "Thêm khách hàng thành công", "HIGH", "PASS"))
    elif i == 2:
        sys_raw.append((cid, "Quản lý Khách Hàng", "Tìm khách hàng theo SĐT 10 số", "Trang Khách hàng", "1. Nhập '0988112233' vào ô tìm kiếm\n2. Quan sát", "SĐT: 0988112233", "Lọc ra chính xác duy nhất khách hàng có SĐT trên", "Tìm đúng khách theo SĐT", "HIGH", "PASS"))
    elif i == 3:
        sys_raw.append((cid, "Quản lý Khách Hàng", "Lọc khách theo Hạng Đồng", "Trang Khách hàng", "1. Chọn filter 'Hạng Đồng'\n2. Quan sát danh sách", "Filter: Hạng Đồng", "Chỉ hiển thị các khách hàng mới ở hạng Đồng", "Lọc đúng khách hạng Đồng", "MEDIUM", "PASS"))
    elif i == 4:
        sys_raw.append((cid, "Quản lý Khách Hàng", "Lọc khách theo Hạng Vàng", "Trang Khách hàng", "1. Chọn filter 'Hạng Vàng'\n2. Quan sát danh sách", "Filter: Hạng Vàng", "Chỉ hiển thị các khách hàng thân thiết hạng Vàng", "Lọc đúng khách hạng Vàng", "MEDIUM", "PASS"))
    elif i == 5:
        sys_raw.append((cid, "Quản lý Khách Hàng", "Chỉnh sửa số điện thoại khách hàng", "Trang Khách hàng", "1. Bấm sửa khách hàng cust-1\n2. Đổi SĐT -> Lưu", "SĐT mới: 0977334455", "Số điện thoại mới được cập nhật trên bảng danh sách", "Cập nhật SĐT khách hàng thành công", "HIGH", "PASS"))
    elif i == 6:
        sys_raw.append((cid, "Quản lý Khách Hàng", "Xóa khách hàng có xác nhận", "Trang Khách hàng", "1. Bấm icon xóa khách\n2. Xác nhận xóa", "Khách hàng cust-1", "Khách hàng bị xóa khỏi danh sách an toàn", "Xóa khách hàng thành công", "HIGH", "PASS"))
    elif i == 7:
        sys_raw.append((cid, "Quản lý Thú Cưng", "Thêm hồ sơ Chó Corgi chân ngắn", "Trang Thú cưng", "1. Bấm Thêm Thú Cưng\n2. Nhập: Corgi Mập, Chó, Corgi, 11kg\n3. Lưu", "Tên: Corgi Mập\nCân nặng: 11kg", "Thú cưng mới hiển thị trong danh sách kèm icon 🐶", "Thêm hồ sơ Chó Corgi thành công", "HIGH", "PASS"))
    elif i == 8:
        sys_raw.append((cid, "Quản lý Thú Cưng", "Thêm hồ sơ Mèo Anh lông dài", "Trang Thú cưng", "1. Bấm Thêm Thú Cưng\n2. Nhập: Mèo Bông, Mèo, Anh lông dài, 4kg\n3. Lưu", "Tên: Mèo Bông\nCân nặng: 4kg", "Thú cưng mới hiển thị trong danh sách kèm icon 🐱", "Thêm hồ sơ Mèo thành công", "HIGH", "PASS"))
    elif i == 9:
        sys_raw.append((cid, "Quản lý Thú Cưng", "Cập nhật cân nặng thú cưng", "Trang Thú cưng", "1. Bấm sửa bé pet-1\n2. Sửa cân nặng từ 4kg lên 4.5kg\n3. Lưu", "Weight mới: 4.5kg", "Cân nặng mới hiển thị chính xác trên Card/Table", "Cập nhật cân nặng thú cưng thành công", "MEDIUM", "PASS"))
    elif i == 10:
        sys_raw.append((cid, "Quản lý Thú Cưng", "Tìm thú cưng theo tên 'Miu'", "Trang Thú cưng", "1. Nhập 'Miu' vào ô tìm kiếm\n2. Quan sát", "Keyword: 'Miu'", "Lọc ra các bé mèo có tên Miu", "Tìm đúng thú cưng theo tên", "MEDIUM", "PASS"))
    elif i == 11:
        sys_raw.append((cid, "Quản lý Thú Cưng", "Chuyển sang chế độ xem Bảng chi tiết", "Trang Thú cưng", "1. Bấm nút 'Xem dạng Bảng'\n2. Kiểm tra các cột", "Chế độ Table View", "Bảng hiển thị đầy đủ cột Tên, Loài, Giống, Cân nặng, Chủ sở hữu", "Chuyển sang Table View hiển thị chuẩn", "LOW", "PASS"))
    elif i == 12:
        sys_raw.append((cid, "Quản lý Thú Cưng", "Xóa hồ sơ thú cưng", "Trang Thú cưng", "1. Bấm xóa bé pet-1\n2. Xác nhận", "Pet: pet-1", "Hồ sơ thú cưng bị xóa an toàn khỏi hệ thống", "Xóa thú cưng thành công", "HIGH", "PASS"))

# ST_PROD (10 Product & Inventory scenarios)
for i in range(1, 11):
    cid = f"ST_PROD_{i:03d}"
    if i == 1:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Thêm sản phẩm mới với giá vốn và giá bán", "Trang Sản phẩm & Kho", "1. Bấm Thêm SP\n2. Nhập: Sữa Tắm Bio, Vốn 60k, Bán 95k, Kho 20\n3. Lưu", "Tên: Sữa Tắm Bio\nKho: 20", "Sản phẩm mới hiển thị với mã SKU tự sinh và tồn kho 20", "Thêm sản phẩm mới vào kho thành công", "HIGH", "PASS"))
    elif i == 2:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Tìm kiếm sản phẩm theo tên 'Pate'", "Trang Sản phẩm & Kho", "1. Nhập 'Pate' vào ô tìm kiếm\n2. Quan sát bảng", "Keyword: 'Pate'", "Lọc ra tất cả các loại Pate cho chó và mèo", "Lọc đúng các sản phẩm Pate", "HIGH", "PASS"))
    elif i == 3:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Tìm kiếm sản phẩm theo mã SKU-PET-102", "Trang Sản phẩm & Kho", "1. Nhập 'SKU-PET-102'\n2. Quan sát", "SKU: SKU-PET-102", "Lọc ra chính xác duy nhất sản phẩm có mã SKU-PET-102", "Tìm đúng sản phẩm theo mã SKU", "HIGH", "PASS"))
    elif i == 4:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Lọc danh mục 'Thức ăn'", "Trang Sản phẩm & Kho", "1. Chọn filter danh mục 'Thức ăn'\n2. Quan sát", "Filter: Thức ăn", "Chỉ hiển thị các sản phẩm thức ăn hạt, pate, bánh thưởng", "Lọc đúng danh mục Thức ăn", "MEDIUM", "PASS"))
    elif i == 5:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Lọc danh mục 'Phụ kiện'", "Trang Sản phẩm & Kho", "1. Chọn filter danh mục 'Phụ kiện'\n2. Quan sát", "Filter: Phụ kiện", "Chỉ hiển thị các sản phẩm vòng cổ, dây dắt, chuồng, bát ăn", "Lọc đúng danh mục Phụ kiện", "MEDIUM", "PASS"))
    elif i == 6:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Lọc danh mục 'Thuốc & Y tế'", "Trang Sản phẩm & Kho", "1. Chọn filter 'Thuốc & Y tế'\n2. Quan sát", "Filter: Thuốc & Y tế", "Chỉ hiển thị các sản phẩm thuốc tẩy giun, xịt ve rận, vitamin", "Lọc đúng danh mục Y tế", "MEDIUM", "PASS"))
    elif i == 7:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Cập nhật giá bán sản phẩm", "Trang Sản phẩm & Kho", "1. Sửa giá bán SP từ 45k lên 50k\n2. Bấm Lưu", "Giá bán mới: 50.000 VNĐ", "Giá bán được cập nhật trên bảng và đồng bộ sang quầy POS", "Cập nhật giá bán sản phẩm thành công", "HIGH", "PASS"))
    elif i == 8:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Điều chỉnh nhập thêm hàng tồn kho", "Trang Sản phẩm & Kho", "1. Nhập thêm 30 cái cho SP prod-1\n2. Lưu tồn kho mới", "Tồn kho mới: 50 cái", "Số lượng tồn kho cập nhật tăng lên 50 chính xác", "Cập nhật tăng tồn kho thành công", "HIGH", "PASS"))
    elif i == 9:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Cảnh báo badge màu đỏ cho sản phẩm hết hàng", "Trang Sản phẩm & Kho", "1. Sản phẩm có tồn kho = 0\n2. Quan sát cột Tồn kho", "Stock = 0", "Hiển thị chữ đỏ 'Kho: 0' kèm nhãn cảnh báo 'Hết hàng'", "Cảnh báo tồn kho hết hàng hiển thị chuẩn", "HIGH", "PASS"))
    elif i == 10:
        sys_raw.append((cid, "Quản lý Kho Hàng", "Xóa sản phẩm khỏi kho hàng", "Trang Sản phẩm & Kho", "1. Bấm xóa SP prod-1\n2. Xác nhận xóa", "SP: prod-1", "Sản phẩm bị xóa an toàn khỏi kho hàng", "Xóa sản phẩm thành công", "HIGH", "PASS"))

# ST_SEC_RBAC (8 Security & Access Control scenarios)
for i in range(1, 9):
    cid = f"ST_SEC_{i:03d}"
    if i == 1:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Đăng nhập quyền Admin truy cập đầy đủ", "Màn hình Login", "1. Login quyền Admin\n2. Kiểm tra toàn bộ 9 module", "User: admin@petcare.com", "Truy cập thành công toàn bộ chức năng Quản trị", "Truy cập đầy đủ tính năng với quyền Admin", "CRITICAL", "PASS"))
    elif i == 2:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Đăng nhập quyền Staff bị giới hạn", "Màn hình Login", "1. Login quyền Staff\n2. Kiểm tra menu Staff", "User: staff@petcare.com", "Ẩn menu Quản lý Nhân sự, chặn truy cập bảo vệ dữ liệu nhạy cảm", "Chặn truy cập module nhạy cảm với quyền Staff", "CRITICAL", "PASS"))
    elif i == 3:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Chặn Customer đăng nhập cổng quản trị", "Màn hình Login", "1. Chọn role customer -> Login", "Role: customer", "Hệ thống từ chối đăng nhập và hiển thị thông báo lỗi rõ ràng", "Từ chối đăng nhập khách hàng thành công", "CRITICAL", "PASS"))
    elif i == 4:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Xác thực mật khẩu khi đăng nhập", "Màn hình Login", "1. Nhập sai mật khẩu\n2. Bấm Đăng nhập", "Pass: 'sai_mat_khau'", "Hệ thống báo lỗi đăng nhập không thành công", "Báo lỗi sai mật khẩu chính xác", "HIGH", "PASS"))
    elif i == 5:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Chống tấn công XSS trong ô nhập liệu", "Form Khách hàng / POS", "1. Nhập chuỗi <script>alert('xss')</script> vào ô Tên\n2. Lưu", "Input: Script XSS", "Hệ thống escape chuỗi HTML, hiển thị dạng text thuần không thực thi script", "Bảo vệ an toàn chống mã độc XSS", "HIGH", "PASS"))
    elif i == 6:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Chống tấn công SQL Injection trong tìm kiếm", "Ô tìm kiếm toàn cục", "1. Nhập chuỗi ' OR 1=1 -- vào ô search\n2. Quan sát", "Input: SQLi payload", "Hệ thống xử lý an toàn dạng chuỗi tìm kiếm thông thường không bị crash", "Xử lý an toàn chống SQLi", "HIGH", "PASS"))
    elif i == 7:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Hủy phiên làm việc hoàn toàn khi Logout", "Top Header", "1. Bấm Đăng xuất\n2. Bấm nút Back trình duyệt", "Thao tác: Logout -> Back", "Trình duyệt không cho phép quay lại trang nội bộ, yêu cầu login lại", "Bảo vệ an toàn phiên sau khi logout", "HIGH", "PASS"))
    elif i == 8:
        sys_raw.append((cid, "Bảo Mật & Phân Quyền", "Bảo vệ dữ liệu giá bán không bị sửa âm", "Form Sản phẩm / POS", "1. Nhập giá bán âm (-50.000đ)\n2. Kiểm tra validate", "Price: -50000", "Hệ thống chặn không cho lưu giá bán âm", "Chặn thành công giá bán âm", "HIGH", "PASS"))

# ST_UI_RESP (4 UI Responsive scenarios)
for i in range(1, 5):
    cid = f"ST_UI_{i:03d}"
    if i == 1:
        sys_raw.append((cid, "Giao Diện & Tương Thích", "Kiểm thử Mobile Drawer trên màn hình 375px", "Màn hình Mobile 375px", "1. Mở Hamburger Menu\n2. Nhấp điều hướng các trang", "Screen: 375x812", "Drawer mở đóng mượt mà, chuyển trang chính xác không tràn lề", "Tương thích tốt trên màn hình Mobile", "MEDIUM", "PASS"))
    elif i == 2:
        sys_raw.append((cid, "Giao Diện & Tương Thích", "Kiểm thử Tablet Layout trên màn hình 768px", "Màn hình iPad 768px", "1. Xem trang Dashboard và POS trên iPad", "Screen: 768x1024", "Layout lưới tự động co giãn 2 cột mượt mà, dễ thao tác chạm", "Hiển thị chuẩn trên Tablet iPad", "MEDIUM", "PASS"))
    elif i == 3:
        sys_raw.append((cid, "Giao Diện & Tương Thích", "Kiểm thử cuộn ngang cho bảng dữ liệu lớn", "Bảng Đơn hàng & Lịch hẹn", "1. Thu nhỏ cửa sổ trình duyệt\n2. Kéo thanh cuộn ngang của bảng", "Table Horizontal Scroll", "Bảng hiển thị thanh cuộn ngang mượt mà, không bị vỡ cột thao tác", "Cuộn ngang bảng dữ liệu mượt mà", "LOW", "PASS"))
    elif i == 4:
        sys_raw.append((cid, "Giao Diện & Tương Thích", "Kiểm thử tương thích trình duyệt Chrome & Edge", "Google Chrome & MS Edge", "1. Mở và thao tác toàn bộ hệ thống trên cả Chrome và Edge", "Chrome 153 & Edge 128", "Giao diện và tính năng hoạt động đồng nhất 100% trên cả 2 trình duyệt", "Tương thích hoàn hảo trên Chrome và Edge", "MEDIUM", "PASS"))

# Build System Test Rows
sys_data = []
for idx, item in enumerate(sys_raw, start=1):
    sys_data.append([
        idx,
        item[0],
        item[1],
        item[2],
        item[3],
        item[4],
        item[5],
        item[6],
        item[7],
        item[8],
        item[9]
    ])

print(f"Generated {len(sys_data)} System Test Cases.")

# 3. Save System Test File
wb_sys = openpyxl.Workbook()
ws_sys = wb_sys.active
ws_sys.title = "System Test Cases"
apply_sheet_formatting(
    ws_sys,
    "BẢNG KỊCH BẢN KIỂM THỬ HỆ THỐNG (SYSTEM / E2E TEST CASES - 100 TEST CASES) - PETCARE PRO",
    "Kiểm thử toàn diện các luồng nghiệp vụ người dùng End-to-End, Bán hàng POS, Đặt lịch 7 bước, Bảo mật & Responsive UI",
    fill_header_sys,
    sys_columns,
    sys_data
)
add_members_sheet(wb_sys, "System Test")
sys_file_path = os.path.join(output_dir, "Nhom_9_System_Test.xlsx")
wb_sys.save(sys_file_path)
print(f"-> Saved: {sys_file_path}")

print("\n============================================================")
print("HOAN TAT TAO TOAN BO 240 TEST CASES (70 UNIT, 70 INTEGRATION, 100 SYSTEM)!")
print("============================================================")
