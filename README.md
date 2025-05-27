1. Tải và cài đặt pgAdmin và PostgreSQL
2. Vào pgAdmin chỗ Server create server với tên plane_db. Copy nội dung trong file  Database trong database_postgresql để tạo csdl.
3. cd vào folder plane-be. Copy lệnh dưới vào terminal.

'''
uvicorn app.main:app --reload

'''

4. Truy cập Swagger:

    http://localhost:8000/docs