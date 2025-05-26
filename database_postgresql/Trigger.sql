-- Các ràng buộc  trigger cho insert, update, delete 

-- 1. Trigger kiểm tra số sân bay trung gian tối đa trong một tuyến bay
-- Giả sử số sân bay trung gian tối đa được lưu trong bảng RULES, và bạn chỉ có 1 dòng duy nhất trong bảng này.
CREATE OR REPLACE FUNCTION trg_check_sanbaytrunggian()
RETURNS TRIGGER AS $$
DECLARE
    max_sanbay INT;
BEGIN
    SELECT SOLUONGSANBAYTRUNGGIANTOIDA INTO max_sanbay FROM RULES LIMIT 1;

    IF (
        SELECT COUNT(*) 
        FROM CHITIETCHUYENBAY 
        WHERE MATUYENBAY = NEW.MATUYENBAY
    ) >= max_sanbay THEN
        RAISE EXCEPTION 'Số lượng sân bay trung gian đã đạt giới hạn cho tuyến bay này';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_chitietchuyenbay
BEFORE INSERT ON CHITIETCHUYENBAY
FOR EACH ROW
EXECUTE FUNCTION trg_check_sanbaytrunggian();

-- 2. Trigger kiểm tra thời gian dừng phù hợp với quy định trong bảng RULES
CREATE OR REPLACE FUNCTION trg_check_thoigiandung()
RETURNS TRIGGER AS $$
DECLARE
    min_dung INT;
    max_dung INT;
BEGIN
    SELECT THOIGIANDUNGTOITHIEU, THOIGIANDUNGTOIDA 
    INTO min_dung, max_dung FROM RULES LIMIT 1;

    IF NEW.THOIGIANDUNG < min_dung OR NEW.THOIGIANDUNG > max_dung THEN
        RAISE EXCEPTION 'Thời gian dừng phải nằm trong khoảng [% - %] phút', min_dung, max_dung;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_thoigiandung
BEFORE INSERT ON CHITIETCHUYENBAY
FOR EACH ROW
EXECUTE FUNCTION trg_check_thoigiandung();

-- 3. Trigger kiểm tra thời gian bay của chuyến bay tối thiểu
CREATE OR REPLACE FUNCTION trg_check_thoigianbay()
RETURNS TRIGGER AS $$
DECLARE
    min_bay INT;
BEGIN
    SELECT THOIGIANBAYTOITHIEU INTO min_bay FROM RULES LIMIT 1;

    IF NEW.THOIGIANBAY < min_bay THEN
        RAISE EXCEPTION 'Thời gian bay phải lớn hơn hoặc bằng % phút', min_bay;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_chuyenbay
BEFORE INSERT ON CHUYENBAY
FOR EACH ROW
EXECUTE FUNCTION trg_check_thoigianbay();

-- 4. Trigger kiểm tra số ghế đặt không vượt quá số ghế trống trong bảng THONGKEHANGVECHUYENBAY
CREATE OR REPLACE FUNCTION trg_check_ghedat()
RETURNS TRIGGER AS $$
DECLARE
    so_ghe_trong INT;
BEGIN
    SELECT SOGHETRONG 
    INTO so_ghe_trong 
    FROM THONGKEHANGVECHUYENBAY
    WHERE MACHUYENBAY = NEW.MACHUYENBAY AND MAHANGVE = NEW.MAHANGVE;

    IF so_ghe_trong IS NULL THEN
        RAISE EXCEPTION 'Không tìm thấy thông tin hạng vé cho chuyến bay';
    END IF;

    IF so_ghe_trong <= 0 THEN
        RAISE EXCEPTION 'Không còn ghế trống';
    END IF;

    -- Giảm số ghế trống, tăng số ghế đã đặt
    UPDATE THONGKEHANGVECHUYENBAY
    SET 
        SOGHETRONG = SOGHETRONG - 1,
        SOGHEDAT = SOGHEDAT + 1
    WHERE MACHUYENBAY = NEW.MACHUYENBAY AND MAHANGVE = NEW.MAHANGVE;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_datve
BEFORE INSERT ON PHIEUDATCHO_VEMAYBAY
FOR EACH ROW
EXECUTE FUNCTION trg_check_ghedat();

-- 5. Trigger khôi phục ghế khi hủy đặt chỗ (chỉ khi chưa lấy vé)
CREATE OR REPLACE FUNCTION trg_huy_dat_ve()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.TRANGTHAILAYVE = FALSE THEN
        UPDATE THONGKEHANGVECHUYENBAY
        SET 
            SOGHETRONG = SOGHETRONG + 1,
            SOGHEDAT = SOGHEDAT - 1
        WHERE MACHUYENBAY = OLD.MACHUYENBAY AND MAHANGVE = OLD.MAHANGVE;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_delete_phieudatcho
BEFORE DELETE ON PHIEUDATCHO_VEMAYBAY
FOR EACH ROW
EXECUTE FUNCTION trg_huy_dat_ve();

-- 6. Không cho phép SANBAYDI = SANBAYDEN trong TUYENBAY
CREATE OR REPLACE FUNCTION trg_check_sanbaydi_den()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.SANBAYDI = NEW.SANBAYDEN THEN
        RAISE EXCEPTION 'Sân bay đi không được trùng với sân bay đến';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_insert_tuyenbay
BEFORE INSERT ON TUYENBAY
FOR EACH ROW
EXECUTE FUNCTION trg_check_sanbaydi_den();


-- 7. Không cho đặt vé sau khi chuyến bay đã bay (so với thời gian hiện tại)
CREATE OR REPLACE FUNCTION trg_kiemtra_ngaydat()
RETURNS TRIGGER AS $$
DECLARE
    ngaybay DATE;
    giobay TIME;
BEGIN
    SELECT NGAYBAY, GIOBAY INTO ngaybay, giobay
    FROM CHUYENBAY WHERE MACHUYENBAY = NEW.MACHUYENBAY;

    IF ngaybay < CURRENT_DATE OR (ngaybay = CURRENT_DATE AND giobay <= CURRENT_TIME) THEN
        RAISE EXCEPTION 'Không thể đặt vé cho chuyến bay đã khởi hành hoặc đang bay';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_kiemtra_thoigian_datve
BEFORE INSERT ON PHIEUDATCHO_VEMAYBAY
FOR EACH ROW
EXECUTE FUNCTION trg_kiemtra_ngaydat();

-- 8. Để tự động cập nhật số ghế đã đặt (SOGHEDAT) trong bảng THONGKEHANGVECHUYENBAY mỗi khi một phiếu đặt chỗ mới được thêm vào
CREATE OR REPLACE FUNCTION trg_tang_soghedat()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE THONGKEHANGVECHUYENBAY
    SET SOGHEDAT = SOGHEDAT + 1
    WHERE MACHUYENBAY = NEW.MACHUYENBAY
      AND MAHANGVE = NEW.MAHANGVE;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_insert_phieudatcho
AFTER INSERT ON PHIEUDATCHO_VEMAYBAY
FOR EACH ROW
EXECUTE FUNCTION trg_tang_soghedat();
