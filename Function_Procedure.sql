------------------------------------------ USE CASE 1 ------------------------------------------
----------------------------------- Tra cứu chuyến bay --------------------------------
CREATE OR REPLACE FUNCTION FUNC_TRA_CUU_CHUYEN_BAY(
    p_sanbaydi VARCHAR DEFAULT NULL,
    p_sanbayden VARCHAR DEFAULT NULL,
    p_ngaybay DATE DEFAULT NULL
)
RETURNS TABLE (
    MACHUYENBAY VARCHAR,
    MATUYENBAY VARCHAR,
    NGAYBAY DATE,
    GIOBAY TIME,
    THOIGIANBAY INT,
    SANBAYDI VARCHAR,
    TENSANBAYDI VARCHAR,
    SANBAYDEN VARCHAR,
    TENSANBAYDEN VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        CB.MACHUYENBAY,
        CB.MATUYENBAY,
        CB.NGAYBAY,
        CB.GIOBAY,
        CB.THOIGIANBAY,
        TB.SANBAYDI,
        SB1.TENSANBAY,
        TB.SANBAYDEN,
        SB2.TENSANBAY
    FROM CHUYENBAY CB
    JOIN TUYENBAY TB ON CB.MATUYENBAY = TB.MATUYENBAY
    JOIN SANBAY SB1 ON TB.SANBAYDI = SB1.MASANBAY
    JOIN SANBAY SB2 ON TB.SANBAYDEN = SB2.MASANBAY
    WHERE (p_sanbaydi IS NULL OR TB.SANBAYDI = p_sanbaydi)
      AND (p_sanbayden IS NULL OR TB.SANBAYDEN = p_sanbayden)
      AND (p_ngaybay IS NULL OR CB.NGAYBAY = p_ngaybay);
END;
$$ LANGUAGE plpgsql;


-- -- Ví dụ 1: Tra cứu tất cả chuyến bay
-- SELECT * FROM FUNC_TRA_CUU_CHUYEN_BAY();

-- -- Ví dụ 2: Tra cứu theo sân bay đi
-- SELECT * FROM FUNC_TRA_CUU_CHUYEN_BAY('SBDI001', NULL, NULL);

-- -- Ví dụ 3: Tra cứu theo ngày bay
-- SELECT * FROM FUNC_TRA_CUU_CHUYEN_BAY(NULL, NULL, '2025-06-01');

-- -- Ví dụ 4: Tra cứu theo sân bay đi, đến và ngày bay
-- SELECT * FROM FUNC_TRA_CUU_CHUYEN_BAY('SBDI001', 'SBDEN001', '2025-06-01');

-- ===========================================================================================--

------------------------------------------ USE CASE 2 ------------------------------------------
------------------------------- Thêm chuyến bay -------------------------------
CREATE OR REPLACE PROCEDURE sp_them_chuyen_bay (
    IN p_machuyenbay VARCHAR,
    IN p_matuyenbay VARCHAR,
    IN p_ngaybay DATE,
    IN p_giobay TIME,
    IN p_thoigianbay INT,
    IN p_soghechuyenbay INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Kiểm tra thông tin đầu vào có bị thiếu không
    IF p_machuyenbay IS NULL OR p_matuyenbay IS NULL OR
       p_ngaybay IS NULL OR p_giobay IS NULL OR
       p_thoigianbay IS NULL OR p_soghechuyenbay IS NULL THEN
        RAISE NOTICE 'Vui lòng nhập chính xác thông tin';
        RETURN;
    END IF;

    -- 2. Kiểm tra thời gian bay và số ghế có hợp lệ không
    IF p_thoigianbay <= 0 OR p_soghechuyenbay <= 0 THEN
        RAISE NOTICE 'Thời gian bay và số ghế phải lớn hơn 0';
        RETURN;
    END IF;

    -- 3. Kiểm tra ngày bay không được nằm trong quá khứ
    IF p_ngaybay < CURRENT_DATE THEN
        RAISE NOTICE 'Không thể thêm chuyến bay với ngày bay trong quá khứ';
        RETURN;
    END IF;

    -- 4. Kiểm tra mã chuyến bay đã tồn tại chưa
    IF EXISTS (SELECT 1 FROM chuyenbay WHERE machuyenbay = p_machuyenbay) THEN
        RAISE NOTICE 'Chuyến bay đã tồn tại';
        RETURN;
    END IF;

    -- 5. Kiểm tra mã tuyến bay có tồn tại không
    IF NOT EXISTS (SELECT 1 FROM tuyenbay WHERE matuyenbay = p_matuyenbay) THEN
        RAISE NOTICE 'Tuyến bay không tồn tại';
        RETURN;
    END IF;

    -- 6. Thêm chuyến bay mới vào bảng CHUYENBAY
    INSERT INTO chuyenbay (
        machuyenbay, matuyenbay, ngaybay, giobay, thoigianbay, soghechuyenbay
    ) VALUES (
        p_machuyenbay, p_matuyenbay, p_ngaybay, p_giobay, p_thoigianbay, p_soghechuyenbay
    );

    -- 7. Thông báo thành công
    RAISE NOTICE 'Đã thêm chuyến bay thành công';
END;
$$;


-- Gọi function
-- CALL sp_them_chuyen_bay(
--     'CB123',
--     'TB001',
--     '2025-06-20',
--     '08:30:00',
--     90,
--     180
-- );

-- ===========================================================================================--

------------------------------------------ USE CASE 3 ------------------------------------------
------------------------------------- Xóa chuyến bay -------------------------------
CREATE OR REPLACE PROCEDURE sp_xoa_chuyen_bay (
    IN p_machuyenbay VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Kiểm tra chuyến bay có tồn tại không
    IF NOT EXISTS (
        SELECT 1 FROM chuyenbay WHERE machuyenbay = p_machuyenbay
    ) THEN
        RAISE NOTICE 'Không tồn tại chuyến bay';
        RETURN;
    END IF;

    -- 2. Xóa các vé/phieu dat cho liên quan đến chuyến bay
    DELETE FROM phieudatcho_vemaybay
    WHERE machuyenbay = p_machuyenbay;

    -- 3. Xóa thống kê hạng vé của chuyến bay
    DELETE FROM thongkehangvechuyenbay
    WHERE machuyenbay = p_machuyenbay;

    -- Không được xóa chi tiết tuyến bay (CHITIETCHUYENBAY) vì không liên quan đến CHUYENBAY

    -- 4. Xóa chuyến bay
    DELETE FROM chuyenbay
    WHERE machuyenbay = p_machuyenbay;

    -- 5. Thông báo
    RAISE NOTICE 'Đã xóa chuyến bay thành công';
END;
$$;

-- CALL sp_xoa_chuyen_bay('CB123');


-- ===========================================================================================--

------------------------------------------ USE CASE 4 ------------------------------------------
------------------------------------- Điều chỉnh chuyến bay -------------------------------
CREATE OR REPLACE PROCEDURE sp_dieu_chinh_chuyen_bay (
    IN p_machuyenbay VARCHAR,
    IN p_matuyenbay VARCHAR,
    IN p_ngaybay DATE,
    IN p_giobay TIME,
    IN p_thoigianbay INT,
    IN p_soghechuyenbay INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Kiểm tra chuyến bay có tồn tại không
    IF NOT EXISTS (
        SELECT 1 FROM chuyenbay WHERE machuyenbay = p_machuyenbay
    ) THEN
        RAISE NOTICE 'Không tồn tại chuyến bay cần chỉnh sửa';
        RETURN;
    END IF;

    -- 2. Kiểm tra tuyến bay có tồn tại không
    IF NOT EXISTS (
        SELECT 1 FROM tuyenbay WHERE matuyenbay = p_matuyenbay
    ) THEN
        RAISE NOTICE 'Tuyến bay không tồn tại';
        RETURN;
    END IF;

    -- 3. Kiểm tra không được điều chỉnh sang ngày bay trong quá khứ
    IF p_ngaybay < CURRENT_DATE THEN
        RAISE NOTICE 'Không thể chỉnh sửa chuyến bay sang ngày trong quá khứ';
        RETURN;
    END IF;

    -- 4. Cập nhật thông tin chuyến bay
    UPDATE chuyenbay
    SET
        matuyenbay = p_matuyenbay,
        ngaybay = p_ngaybay,
        giobay = p_giobay,
        thoigianbay = p_thoigianbay,
        soghechuyenbay = p_soghechuyenbay
    WHERE machuyenbay = p_machuyenbay;

    -- 5. Thông báo thành công
    RAISE NOTICE 'Chỉnh sửa thông tin chuyến bay thành công';
END;
$$;

-- CALL sp_dieu_chinh_chuyen_bay(
--     'CB123',        -- Mã chuyến bay cần chỉnh sửa
--     'TB001',        -- Tuyến bay mới
--     '2025-06-01',   -- Ngày bay mới
--     '08:30',        -- Giờ bay mới
--     90,             -- Thời gian bay mới
--     180             -- Số ghế mới
-- );


-- ===========================================================================================--

------------------------------------------ USE CASE 5 ------------------------------------------
------------------------------------- Tra cứu phiếu đặt chỗ -------------------------------
CREATE OR REPLACE FUNCTION f_tra_cuu_phieu_datcho(
    p_tenhanhkhach VARCHAR,
    p_cmnd_cccd VARCHAR,
    p_sodienthoai VARCHAR,
    p_gioitinh VARCHAR
)
RETURNS TABLE (
    maphieudatcho VARCHAR,
    machuyenbay VARCHAR,
    tenhanhkhach VARCHAR,
    cmnd_cccd VARCHAR,
    gioitinh VARCHAR,
    sodienthoai VARCHAR,
    mahangve VARCHAR,
    giatien BIGINT,
    ngaydat DATE,
    trangthailayve BOOLEAN,
    idnhanvien VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Kiểm tra xem có phiếu đặt chỗ nào phù hợp không
    IF NOT EXISTS (
        SELECT 1
        FROM PHIEUDATCHO_VEMAYBAY
        WHERE tenhanhkhach = p_tenhanhkhach
          AND cmnd_cccd = p_cmnd_cccd
          AND sodienthoai = p_sodienthoai
          AND gioitinh = p_gioitinh
    ) THEN
        RAISE NOTICE 'Không tìm thấy phiếu đặt chỗ. Vui lòng nhập lại thông tin chính xác.';
        RETURN;
    END IF;

    -- Trả về danh sách phiếu đặt chỗ phù hợp
    RETURN QUERY
    SELECT
        maphieudatcho,
        machuyenbay,
        tenhanhkhach,
        cmnd_cccd,
        gioitinh,
        sodienthoai,
        mahangve,
        giatien,
        ngaydat,
        trangthailayve,
        idnhanvien
    FROM PHIEUDATCHO_VEMAYBAY
    WHERE tenhanhkhach = p_tenhanhkhach
      AND cmnd_cccd = p_cmnd_cccd
      AND sodienthoai = p_sodienthoai
      AND gioitinh = p_gioitinh;
END;
$$;

-- -- Ví dụ gọi tra cứu phiếu đặt chỗ mã "PDC001"
-- SELECT * FROM f_tra_cuu_phieu_datcho(
--     'Nguyen Van A',
--     '012345678901',
--     '0901234567',
--     'Nam'
-- );





-- ===========================================================================================--

------------------------------------------ USE CASE 6 ------------------------------------------
------------------------------------- Tạo phiếu đặt chỗ -------------------------------
-- Procedure tạo phiếu đặt chỗ mới nếu chưa tồn tại
CREATE OR REPLACE PROCEDURE tao_phieu_datcho(
    p_maphieu VARCHAR,
    p_machuyenbay VARCHAR,
    p_tenhanhkhach VARCHAR,
    p_cmnd_cccd VARCHAR,
    p_gioitinh VARCHAR,
    p_sodienthoai VARCHAR,
    p_mahangve VARCHAR,
    p_giatien BIGINT,
    p_ngaydat DATE,
    p_trangthailayve BOOLEAN,
    p_idnhanvien VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_exists BOOLEAN;
BEGIN
    -- Bước 1: Kiểm tra phiếu đặt chỗ đã tồn tại hay chưa
    SELECT EXISTS (
        SELECT 1 FROM PHIEUDATCHO_VEMAYBAY WHERE MAPHIEUDATCHO = p_maphieu
    ) INTO v_exists;

    IF v_exists THEN
        -- Nếu đã tồn tại thì thông báo lỗi và dừng
        RAISE NOTICE 'Phiếu đặt chỗ đã tồn tại.';
        RETURN;
    END IF;

    -- Bước 2: Thêm phiếu đặt chỗ vào bảng
    INSERT INTO PHIEUDATCHO_VEMAYBAY (
        MAPHIEUDATCHO, MACHUYENBAY, TENHANHKHACH, CMND_CCCD, GIOITINH,
        SODIENTHOAI, MAHANGVE, GIATIEN, NGAYDAT, TRANGTHAILAYVE, IDNHANVIEN
    ) VALUES (
        p_maphieu, p_machuyenbay, p_tenhanhkhach, p_cmnd_cccd, p_gioitinh,
        p_sodienthoai, p_mahangve, p_giatien, p_ngaydat, p_trangthailayve, p_idnhanvien
    );

    -- Bước 3: Thông báo thành công
    RAISE NOTICE 'Tạo phiếu đặt chỗ thành công.';
EXCEPTION
    -- Nếu có lỗi định dạng hoặc lỗi ràng buộc, thì hiển thị thông báo phù hợp
    WHEN others THEN
        RAISE NOTICE 'Vui lòng nhập chính xác thông tin. Lỗi: %', SQLERRM;
END;
$$;


-- CALL tao_phieu_datcho(
--     'PD003',                -- MAPHIEUDATCHO
--     'CB001',                -- MACHUYENBAY
--     'Trần Thị B',           -- TENHANHKHACH
--     '987654321',            -- CMND_CCCD
--     'Nữ',                   -- GIOITINH
--     '0987654321',           -- SODIENTHOAI
--     'HV002',                -- MAHANGVE
--     2000000,                -- GIATIEN
--     CURRENT_DATE,           -- NGAYDAT
--     FALSE,                  -- TRANGTHAILAYVE
--     'NV002'                 -- IDNHANVIEN
-- );


-- ===========================================================================================--


------------------------------------------ USE CASE 7 ------------------------------------------
------------------------------------- Xóa phiếu đặt chỗ -------------------------------
 
-- Procedure xóa phiếu đặt chỗ nếu tồn tại
CREATE OR REPLACE PROCEDURE xoa_phieu_datcho(
    p_maphieudatcho VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_exists BOOLEAN;
BEGIN
    -- Bước 1: Kiểm tra phiếu đặt chỗ có tồn tại hay không
    SELECT EXISTS (
        SELECT 1 FROM PHIEUDATCHO_VEMAYBAY WHERE MAPHIEUDATCHO = p_maphieudatcho
    ) INTO v_exists;

    IF NOT v_exists THEN
        -- Nếu không tồn tại thì thông báo và dừng procedure
        RAISE NOTICE 'Không tồn tại phiếu đặt chỗ.';
        RETURN;
    END IF;

    -- Bước 2: Xóa phiếu đặt chỗ
    DELETE FROM PHIEUDATCHO_VEMAYBAY
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    -- Bước 3: Thông báo thành công
    RAISE NOTICE 'Đã xóa phiếu đặt chỗ thành công.';
EXCEPTION
    -- Nếu xảy ra lỗi trong quá trình xóa, thông báo lỗi
    WHEN OTHERS THEN
        RAISE NOTICE 'Lỗi khi xóa phiếu đặt chỗ: %', SQLERRM;
END;
$$;


-- CALL xoa_phieu_datcho('PD003');



------------------------------------------ USE CASE 8 ------------------------------------------
----------------------------------- Chỉnh sửa phiếu đặt chỗ -------------------------------
-- Procedure cập nhật thông tin phiếu đặt chỗ nếu tồn tại
CREATE OR REPLACE PROCEDURE chinhsua_phieu_datcho(
    p_maphieudatcho VARCHAR,
    p_machuyenbay VARCHAR,
    p_tenhanhkhach VARCHAR,
    p_cmnd_cccd VARCHAR,
    p_gioitinh VARCHAR,
    p_sodienthoai VARCHAR,
    p_mahangve VARCHAR,
    p_giatien BIGINT,
    p_ngaydat DATE,
    p_trangthailayve BOOLEAN,
    p_idnhanvien VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_exists BOOLEAN;
BEGIN
    -- Bước 1: Kiểm tra xem phiếu đặt chỗ có tồn tại không
    SELECT EXISTS (
        SELECT 1 FROM PHIEUDATCHO_VEMAYBAY WHERE MAPHIEUDATCHO = p_maphieudatcho
    ) INTO v_exists;

    IF NOT v_exists THEN
        -- Nếu phiếu không tồn tại thì thông báo và thoát procedure
        RAISE NOTICE 'Không tồn tại phiếu đặt chỗ.';
        RETURN;
    END IF;

    -- Bước 2: Cập nhật thông tin phiếu đặt chỗ
    UPDATE PHIEUDATCHO_VEMAYBAY
    SET
        MACHUYENBAY = p_machuyenbay,
        TENHANHKHACH = p_tenhanhkhach,
        CMND_CCCD = p_cmnd_cccd,
        GIOITINH = p_gioitinh,
        SODIENTHOAI = p_sodienthoai,
        MAHANGVE = p_mahangve,
        GIATIEN = p_giatien,
        NGAYDAT = p_ngaydat,
        TRANGTHAILAYVE = p_trangthailayve,
        IDNHANVIEN = p_idnhanvien
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    -- Bước 3: Thông báo cập nhật thành công
    RAISE NOTICE 'Chỉnh sửa phiếu đặt chỗ thành công.';
EXCEPTION
    -- Nếu xảy ra lỗi trong quá trình chỉnh sửa
    WHEN OTHERS THEN
        RAISE NOTICE 'Lỗi khi chỉnh sửa phiếu đặt chỗ: %', SQLERRM;
END;
$$;


-- CALL chinhsua_phieu_datcho(
--     'PD001',
--     'CB001',
--     'Nguyễn Văn A',
--     '123456789',
--     'Nam',
--     '0901234567',
--     'HV1',
--     1200000,
--     CURRENT_DATE,
--     TRUE,
--     'NV001'
-- );



------------------------------------------ USE CASE 9 ------------------------------------------
----------------------------- Xuất vé chuyến bay từ phiếu đặt chỗ -------------------------------

-- Function dùng để xuất vé từ phiếu đặt chỗ
CREATE OR REPLACE PROCEDURE sp_xuat_ve_tu_phieu(p_maphieudatcho VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_exists BOOLEAN;
    v_daxuatve BOOLEAN;
BEGIN
    -- Kiểm tra phiếu có tồn tại không
    SELECT TRUE INTO v_exists
    FROM PHIEUDATCHO_VEMAYBAY
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    IF NOT FOUND THEN
        RAISE NOTICE 'Không tồn tại phiếu đặt chỗ.';
        RETURN;
    END IF;

    -- Kiểm tra đã xuất vé chưa
    SELECT TRANGTHAILAYVE INTO v_daxuatve
    FROM PHIEUDATCHO_VEMAYBAY
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    IF v_daxuatve THEN
        RAISE NOTICE 'Vé đã được xuất trước đó.';
        RETURN;
    END IF;

    -- Cập nhật trạng thái
    UPDATE PHIEUDATCHO_VEMAYBAY
    SET TRANGTHAILAYVE = TRUE
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    RAISE NOTICE 'Xuất vé thành công.';
END;
$$;

-- CALL sp_xuat_ve_tu_phieu('PHIEU001');

-- ===========================================================================================--

------------------------------------------ USE CASE 10 ------------------------------------------
------------------------------------- Tra cứu vé chuyến bay -------------------------------
CREATE OR REPLACE FUNCTION fn_tra_cuu_ve(
    p_tenhanhkhach VARCHAR,
    p_cmnd_cccd VARCHAR,
    p_sodienthoai VARCHAR,
    p_gioitinh VARCHAR
)
RETURNS TABLE (
    maphieudatcho VARCHAR,
    machuyenbay VARCHAR,
    tenhanhkhach VARCHAR,
    cmnd_cccd VARCHAR,
    gioitinh VARCHAR,
    sodienthoai VARCHAR,
    mahangve VARCHAR,
    giatien INT,
    ngaydat DATE,
    idnhanvien VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        maphieudatcho,
        machuyenbay,
        tenhanhkhach,
        cmnd_cccd,
        gioitinh,
        sodienthoai,
        mahangve,
        giatien,
        ngaydat,
        idnhanvien
    FROM phieudatcho_vemaybay
    WHERE trangthailayve = TRUE
      AND (p_tenhanhkhach IS NULL OR tenhanhkhach ILIKE '%' || p_tenhanhkhach || '%')
      AND (p_cmnd_cccd IS NULL OR cmnd_cccd = p_cmnd_cccd)
      AND (p_sodienthoai IS NULL OR sodienthoai = p_sodienthoai)
      AND (p_gioitinh IS NULL OR gioitinh = p_gioitinh);
END;
$$ LANGUAGE plpgsql;

-- -- Tra cứu vé với đầy đủ thông tin:
-- SELECT * FROM fn_tra_cuu_ve('Nguyen Van A', '0123456789', '0912345678', 'Nam');

-- -- Tra cứu theo một phần tên, bỏ qua CCCD và số điện thoại:
-- SELECT * FROM fn_tra_cuu_ve('Nguyen', NULL, NULL, NULL);

-- ===========================================================================================--

------------------------------------------ USE CASE 11 ------------------------------------------
------------------------------------- Hủy vé chuyến bay -------------------------------
CREATE OR REPLACE PROCEDURE PROC_HUY_VE_CHUYEN_BAY(
    IN p_maphieudatcho VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Kiểm tra vé có tồn tại và đã được xuất chưa
    IF NOT EXISTS (
        SELECT 1 FROM PHIEUDATCHO_VEMAYBAY
        WHERE MAPHIEUDATCHO = p_maphieudatcho AND TRANGTHAILAYVE = TRUE
    ) THEN
        RAISE EXCEPTION 'Không tồn tại vé chuyến bay hoặc vé chưa được xuất.';
    END IF;

    -- Xóa vé
    DELETE FROM PHIEUDATCHO_VEMAYBAY
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    RAISE NOTICE 'Đã hủy vé chuyến bay thành công.';
END;
$$;

-- -- Gọi procedure để hủy một vé
-- CALL PROC_HUY_VE_CHUYEN_BAY('PD001');

-- ===========================================================================================--

------------------------------------------ USE CASE 12 ------------------------------------------
------------------------------------- Chỉnh sửa thông tin vé chuyến bay  -------------------------------
CREATE OR REPLACE PROCEDURE PROC_CHINH_SUA_VE_CHUYEN_BAY(
    IN p_maphieudatcho VARCHAR,
    IN p_tenhanhkhach VARCHAR,
    IN p_cmnd_cccd VARCHAR,
    IN p_gioitinh VARCHAR,
    IN p_sodienthoai VARCHAR,
    IN p_mahangve VARCHAR,
    IN p_giatien BIGINT,
    IN p_idnhanvien VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Kiểm tra xem vé có tồn tại và đã được xuất hay chưa
    IF NOT EXISTS (
        SELECT 1 FROM PHIEUDATCHO_VEMAYBAY
        WHERE MAPHIEUDATCHO = p_maphieudatcho AND TRANGTHAILAYVE = TRUE
    ) THEN
        RAISE EXCEPTION 'Không tồn tại vé chuyến bay hoặc vé chưa được xuất.';
    END IF;

    -- Cập nhật thông tin vé chuyến bay
    UPDATE PHIEUDATCHO_VEMAYBAY
    SET
        TENHANHKHACH = p_tenhanhkhach,
        CMND_CCCD = p_cmnd_cccd,
        GIOITINH = p_gioitinh,
        SODIENTHOAI = p_sodienthoai,
        MAHANGVE = p_mahangve,
        GIATIEN = p_giatien,
        IDNHANVIEN = p_idnhanvien
    WHERE MAPHIEUDATCHO = p_maphieudatcho;

    RAISE NOTICE 'Thông tin vé chuyến bay đã được cập nhật thành công.';
END;
$$;

-- CALL PROC_CHINH_SUA_VE_CHUYEN_BAY(
--     'PD001',
--     'Nguyễn Văn A',
--     '123456789',
--     'Nam',
--     '0912345678',
--     'HV1',
--     1500000,
--     'NV01'
-- );



-- ===========================================================================================--

------------------------------------------ USE CASE 13 ------------------------------------------
------------------------------------- Xem báo cáo doanh thu tháng  -------------------------------
CREATE OR REPLACE FUNCTION FUNC_BAOCAO_DOANHTHU_THANG(
    p_thang INT,
    p_nam INT
)
RETURNS TABLE (
    MACHUYENBAY VARCHAR,
    SOVE INT,
    TYLE NUMERIC(5,2),
    DOANHTHU BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cb.MACHUYENBAY,
        COUNT(pv.MAPHIEUDATCHO) AS SOVE,
        ROUND(COUNT(pv.MAPHIEUDATCHO)::NUMERIC / NULLIF(cb.SOGHECHUYENBAY, 0) * 100, 2) AS TYLE,
        SUM(pv.GIATIEN) AS DOANHTHU
    FROM PHIEUDATCHO_VEMAYBAY pv
    JOIN CHUYENBAY cb ON pv.MACHUYENBAY = cb.MACHUYENBAY
    WHERE pv.TRANGTHAILAYVE = TRUE
      AND EXTRACT(MONTH FROM pv.NGAYDAT) = p_thang
      AND EXTRACT(YEAR FROM pv.NGAYDAT) = p_nam
    GROUP BY cb.MACHUYENBAY, cb.SOGHECHUYENBAY;

    -- Nếu không có dữ liệu, trả thông báo lỗi
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Không tồn tại doanh thu trong tháng % và năm %.', p_thang, p_nam;
    END IF;
END;
$$;

-- SELECT * FROM FUNC_BAOCAO_DOANHTHU_THANG(5, 2025);


-- ===========================================================================================--

------------------------------------------ USE CASE 14 ------------------------------------------
------------------------------------- Xem báo cáo doanh thu năm  -------------------------------
CREATE OR REPLACE FUNCTION baocao_doanhthu_nam(nam INTEGER)
RETURNS TABLE (
    thang INTEGER,
    sochuyenbay INTEGER,
    doanhthu_thucte BIGINT,
    doanhthu_toida BIGINT,
    tyle_doanhthu NUMERIC(5, 2)  -- phần trăm
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH chuyenbay_theothang AS (
        SELECT 
            cb.machuyenbay,
            EXTRACT(MONTH FROM cb.ngaybay)::INT AS thang
        FROM chuyenbay cb
        WHERE EXTRACT(YEAR FROM cb.ngaybay)::INT = nam
          AND (
              nam < EXTRACT(YEAR FROM CURRENT_DATE)::INT
              OR EXTRACT(MONTH FROM cb.ngaybay)::INT < EXTRACT(MONTH FROM CURRENT_DATE)::INT
          )
    ),

    doanhthu_thucte_theothang AS (
        SELECT 
            EXTRACT(MONTH FROM cb.ngaybay)::INT AS thang,
            COUNT(DISTINCT cb.machuyenbay) AS sochuyenbay,
            SUM(p.giatien) AS doanhthu_thucte
        FROM phieudatcho_vemaybay p
        JOIN chuyenbay cb ON p.machuyenbay = cb.machuyenbay
        WHERE p.trangthailayve = TRUE
          AND EXTRACT(YEAR FROM cb.ngaybay)::INT = nam
          AND (
              nam < EXTRACT(YEAR FROM CURRENT_DATE)::INT
              OR EXTRACT(MONTH FROM cb.ngaybay)::INT < EXTRACT(MONTH FROM CURRENT_DATE)::INT
          )
        GROUP BY EXTRACT(MONTH FROM cb.ngaybay)
    ),

    doanhthu_toida_theothang AS (
        SELECT 
            EXTRACT(MONTH FROM cb.ngaybay)::INT AS thang,
            SUM(tkv.soluongghe * dg.giatien) AS doanhthu_toida
        FROM chuyenbay cb
        JOIN thongkehangvechuyenbay tkv ON cb.machuyenbay = tkv.machuyenbay
        JOIN dongia dg ON cb.matuyenbay = dg.matuyenbay AND tkv.mahangve = dg.mahangve
        WHERE EXTRACT(YEAR FROM cb.ngaybay)::INT = nam
          AND (
              nam < EXTRACT(YEAR FROM CURRENT_DATE)::INT
              OR EXTRACT(MONTH FROM cb.ngaybay)::INT < EXTRACT(MONTH FROM CURRENT_DATE)::INT
          )
        GROUP BY EXTRACT(MONTH FROM cb.ngaybay)
    )

    SELECT 
        COALESCE(dtt.thang, dtd.thang, dttt.thang) AS thang,
        COALESCE(dtt.sochuyenbay, 0) AS sochuyenbay,
        COALESCE(dtt.doanhthu_thucte, 0) AS doanhthu_thucte,
        COALESCE(dtd.doanhthu_toida, 0) AS doanhthu_toida,
        ROUND(
            CASE 
                WHEN COALESCE(dtd.doanhthu_toida, 0) = 0 THEN 0
                ELSE COALESCE(dtt.doanhthu_thucte, 0) * 100.0 / dtd.doanhthu_toida
            END, 2
        ) AS tyle_doanhthu
    FROM doanhthu_thucte_theothang dtt
    FULL OUTER JOIN doanhthu_toida_theothang dtd ON dtt.thang = dtd.thang
    FULL OUTER JOIN (
        SELECT DISTINCT thang FROM chuyenbay_theothang
    ) dttt ON dttt.thang = dtt.thang OR dttt.thang = dtd.thang
    ORDER BY thang;
END;
$$;

-- SELECT * FROM baocao_doanhthu_nam(2024);

-- ===========================================================================================--

------------------------------------------ USE CASE 15 ------------------------------------------
------------------------------------- Đăng nhập tài khoản  -------------------------------
CREATE OR REPLACE FUNCTION dangnhap_taikhoan(
    p_tendangnhap VARCHAR,
    p_matkhau VARCHAR
)
RETURNS TABLE (
    ketqua TEXT,
    idnhanvien VARCHAR,
    tennhanvien VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_tendangnhap IS NULL OR p_matkhau IS NULL OR TRIM(p_tendangnhap) = '' OR TRIM(p_matkhau) = '' THEN
        RETURN QUERY SELECT 'Bạn cần phải nhập cả Tên người dùng và Mật khẩu để đăng nhập tài khoản', NULL, NULL;
        RETURN;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM taikhoannhanvien WHERE tendangnhap = p_tendangnhap
    ) THEN
        RETURN QUERY SELECT 'Sai tên người dùng. Vui lòng nhập lại.', NULL, NULL;
        RETURN;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM taikhoannhanvien 
        WHERE tendangnhap = p_tendangnhap AND matkhau = p_matkhau
    ) THEN
        RETURN QUERY SELECT 'Sai mật khẩu. Vui lòng nhập lại.', NULL, NULL;
        RETURN;
    END IF;

    -- Đăng nhập thành công
    RETURN QUERY 
    SELECT 
        'Đăng nhập thành công' AS ketqua, 
        idnhanvien, 
        tennhanvien
    FROM taikhoannhanvien 
    WHERE tendangnhap = p_tendangnhap AND matkhau = p_matkhau
    LIMIT 1;
END;
$$;


-- SELECT * FROM dangnhap_taikhoan('admin123', '123456');

-- ===========================================================================================--

------------------------------------------ USE CASE 16 ------------------------------------------
------------------------------------- Đăng xuất tài khoản  -------------------------------

CREATE TABLE IF NOT EXISTS session_dangnhap_tam (
    idnhanvien VARCHAR PRIMARY KEY,
    thoigiandangnhap TIMESTAMP DEFAULT now()
);


CREATE OR REPLACE PROCEDURE dangxuat_taikhoan(p_idnhanvien VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM session_dangnhap_tam WHERE idnhanvien = p_idnhanvien) THEN
        RAISE NOTICE 'Chưa đăng nhập. Không thể thực hiện đăng xuất.';
    ELSE
        DELETE FROM session_dangnhap_tam WHERE idnhanvien = p_idnhanvien;
        RAISE NOTICE 'Đăng xuất thành công.';
    END IF;
END;
$$;

-- CALL dangxuat_taikhoan('NV001');

-- ===========================================================================================--

------------------------------------------ USE CASE 17 ------------------------------------------
------------------------------------- Thay đổi quy định  -------------------------------

CREATE OR REPLACE PROCEDURE capnhat_quydinh(
    p_sb_toida INT,
    p_sb_trunggian_toida INT,
    p_tgbay_toithieu INT,
    p_tgdung_toida INT,
    p_tgdung_toithieu INT,
    p_tgdatve_chamnhat INT,
    p_tghuydatve_chamnhat INT,
    OUT ketqua TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Kiểm tra logic
    IF p_sb_toida < 0 OR p_sb_trunggian_toida < 0 THEN
        ketqua := 'Lỗi: Số lượng sân bay không hợp lệ.';
        RETURN;
    END IF;

    IF p_tgbay_toithieu <= 0 THEN
        ketqua := 'Lỗi: Thời gian bay tối thiểu phải lớn hơn 0.';
        RETURN;
    END IF;

    IF p_tgdung_toithieu <= 0 THEN
        ketqua := 'Lỗi: Thời gian dừng tối thiểu phải lớn hơn 0.';
        RETURN;
    END IF;

    IF p_tgdung_toida < p_tgdung_toithieu THEN
        ketqua := 'Lỗi: Thời gian dừng tối đa phải lớn hơn hoặc bằng thời gian dừng tối thiểu.';
        RETURN;
    END IF;

    IF p_tgdatve_chamnhat <= 0 OR p_tghuydatve_chamnhat <= 0 THEN
        ketqua := 'Lỗi: Thời gian đặt/hủy vé chậm nhất phải lớn hơn 0.';
        RETURN;
    END IF;

    -- Cập nhật
    UPDATE RULES
    SET 
        SOLUONGSANBAYTOIDA = p_sb_toida,
        SOLUONGSANBAYTRUNGGIANTOIDA = p_sb_trunggian_toida,
        THOIGIANBAYTOITHIEU = p_tgbay_toithieu,
        THOIGIANDUNGTOIDA = p_tgdung_toida,
        THOIGIANDUNGTOITHIEU = p_tgdung_toithieu,
        THOIGIANCHAMNHATDATVE = p_tgdatve_chamnhat,
        THOIGIANCHAMNHATHUYDATVE = p_tghuydatve_chamnhat;

    ketqua := 'Cập nhật quy định thành công.';
END;
$$;


-- CALL capnhat_quydinh(
--     12, -- SOLUONGSANBAYTOIDA
--     3,  -- SOLUONGSANBAYTRUNGGIANTOIDA
--     35, -- THOIGIANBAYTOITHIEU
--     25, -- THOIGIANDUNGTOIDA
--     15, -- THOIGIANDUNGTOITHIEU
--     2,  -- THOIGIANCHAMNHATDATVE
--     2,  -- THOIGIANCHAMNHATHUYDATVE
--     NULL -- OUT: ketqua
-- );



-- ===========================================================================================--

------------------------------------------ Các Function và Procedure hỗ trợ  ------------------------------------------
-- (có thể sư dụng function sau để lấy thông tin trận dấu chưa được ghi nhận)
-- . Lấy ra k trận đấu chưa được thi đấu (hoặc chưa được ghi nhận)
-- CREATE OR REPLACE FUNCTION get_unplayed_matches(k INT)
-- RETURNS TABLE (
-- 	match_id INT, 
--     home_team_name VARCHAR,
--     away_team_name VARCHAR,
--     time_start TIME,
--     day_start DATE,
--     stadium_name VARCHAR
-- ) AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT 
-- 		m.id AS match_id, 
--         ht.name AS home_team_name,
--         at.name AS away_team_name,
--         m.time_start,
--         m.day_start,
--         m.stadium_name
--     FROM 
--         Match m
--     JOIN Team ht ON m.home_team_id = ht.id
--     JOIN Team at ON m.away_team_id = at.id
--     WHERE 
--         m.id IN (
--             SELECT id FROM match
--             EXCEPT
--             SELECT id FROM match_result
--         )
--     ORDER BY 
--         m.day_start ASC, m.time_start ASC  
--     LIMIT k;  
-- END;
-- $$ LANGUAGE plpgsql;

-- -- 4. tra cứu thông tin đội bóng
-- CREATE OR REPLACE FUNCTION search_team_by_name(search_name VARCHAR)
-- RETURNS TABLE(
-- 	name VARCHAR, 
-- 	stadium_name VARCHAR
-- ) AS $$
-- BEGIN
-- 	RETURN QUERY 
-- 	SELECT 
-- 		t.name,
-- 		T.stadium_name
-- 	FROM 
-- 		Team t 
-- 	WHERE 
-- 		t.name ILIKE '%' || search_name || '%';
-- END
-- $$ LANGUAGE plpgsql;

-- -- 6: Lấy ra các cầu thủ ghi bàn với ID trận đấu. 
-- CREATE OR REPLACE FUNCTION get_goal_by_id_match(search_id INT)
-- RETURNS TABLE (
--     team_id INT,
--     player_id INT,
--     player_name VARCHAR,
--     goal_time INT,
--     goal_type VARCHAR
-- ) AS $$
-- BEGIN 
--     RETURN QUERY
--     SELECT 
--         g.team_id,
--         g.player_id,
--         p.name AS player_name,
--         g.time AS goal_time,
--         g.type AS goal_type
--     FROM 
--         Goal g
--     JOIN 
--         Player p ON p.id = g.player_id AND p.team_id = g.team_id
--     WHERE 
--         g.match_id = search_id;
-- END;
-- $$ LANGUAGE plpgsql; 







