-- B1: Tạo bảng + PK
CREATE TABLE Rules
(
	max_airports INT DEFAULT 10 CHECK (max_airports >= 0),
	max_transit_airports INT DEFAULT 2 CHECK (max_transit_airports >= 0),
    min_flight_time INT DEFAULT 30 CHECK (min_flight_time > 0),
	min_stop_time INT DEFAULT 10 CHECK (min_stop_time > 0),
	max_stop_time INT DEFAULT 20 CHECK (max_stop_time >= min_stop_time),
    latest_booking_time INT DEFAULT 1 CHECK (latest_booking_time > 0),
	latest_cancel_time INT DEFAULT 1 CHECK (latest_cancel_time > 0),
	ticket_class_count INT DEFAULT 2 CHECK (ticket_class_count > 0)
);

CREATE TABLE Airport
(
	airport_id VARCHAR(50) NOT NULL,
	airport_name VARCHAR(50) NOT NULL,
	airport_address VARCHAR(50) NOT NULL,
	CONSTRAINT PK_Airport PRIMARY KEY (airport_id)
);


CREATE TABLE FlightRoute
(
	flight_route_id VARCHAR(50) NOT NULL,
	departure_airport_id VARCHAR(50) NOT NULL,
	arrival_airport_id VARCHAR(50) NOT NULL,
	CONSTRAINT PK_FlightRoute PRIMARY KEY (flight_route_id)
);

CREATE TABLE Flight
(
	flight_id VARCHAR(50) NOT NULL,
	flight_route_id VARCHAR(50) NOT NULL,
	flight_date DATE NOT NULL,
	departure_time TIME NOT NULL,
	flight_duration INT NOT NULL,
	flight_seat_count INT NOT NULL,
	CONSTRAINT PK_Flight PRIMARY KEY (flight_id)
);

CREATE TABLE FlightDetail
(
	flight_detail_id VARCHAR(50) NOT NULL,
	flight_route_id VARCHAR(50) NOT NULL,
	transit_airport_id VARCHAR(50) NOT NULL,
	stop_time INT NOT NULL,
	note VARCHAR(200),
	CONSTRAINT PK_FlightDetail PRIMARY KEY (flight_detail_id)
);

CREATE TABLE TicketClass
(
	ticket_class_id VARCHAR(50) NOT NULL,
	ticket_class_name VARCHAR(50) NOT NULL,
	CONSTRAINT PK_TicketClass PRIMARY KEY (ticket_class_id)
);

CREATE TABLE TicketClassStatistics
(
	ticket_class_statistics_id varchar(50) NOT NULL,
	flight_id VARCHAR(50) NOT NULL,
	ticket_class_id VARCHAR(50) NOT NULL,
	total_seats INT NOT NULL,	-- Số lượng ghế của hạng vé trong chuyến bay đó --
	available_seats INT NOT NULL,	-- Số lượng ghế trống của hạng vé đó --
	booked_seats INT NOT NULL,		-- Số lượng ghế đã đặt, lấy từ các phiếu đặt chỗ của chuyến bay --
	CONSTRAINT PK_TicketClassStatistics PRIMARY KEY (ticket_class_statistics_id)
);

CREATE TABLE TicketPrice
(
	ticket_price_id VARCHAR(50) NOT NULL,
	flight_route_id VARCHAR(50) NOT NULL,
	ticket_class_id VARCHAR(50) NOT NULL,
	price INT NOT NULL,
	CONSTRAINT PK_TicketPrice PRIMARY KEY (ticket_price_id)
);

CREATE TABLE Employee
(
	employee_id VARCHAR(50) NOT NULL,
	employee_username VARCHAR(200) NOT NULL,
	employee_password VARCHAR(200) NOT NULL,
	employee_name VARCHAR(50) NOT NULL,
	national_id VARCHAR(50) NOT NULL,
	gender VARCHAR(3) CHECK (Gender IN ('Nam', 'Nữ')),
	phone_number VARCHAR(50) NOT NULL,
	created_date DATE NOT NULL,
	CONSTRAINT PK_Employee PRIMARY KEY (employee_id)
);

CREATE TABLE Booking_Ticket
(
	booking_ticket_id VARCHAR(50) NOT NULL,
	flight_id VARCHAR(50) NOT NULL,
	-- Thông tin Hành khách
	passenger_name VARCHAR(50) NOT NULL,
	national_id VARCHAR(50) NOT NULL,
	gender VARCHAR(3) CHECK (Gender IN ('Nam', 'Nữ')),
	phone_number VARCHAR(12) NOT NULL,
	-- Thông tin vé
	ticket_class_id VARCHAR(50) NOT NULL,
	booking_price BIGINT NOT NULL,
	booking_date DATE NOT NULL,
	-- -- Quan trọng: True (Đã xuất vé - Là vé chuyến bay), False (Chỉ là phiếu đặt chỗ)
	ticket_status BOOLEAN NOT NULL,
	-- Thông tin nhân viên
	employee_id VARCHAR(50) NOT NULL,
	CONSTRAINT PK_Booking_Ticket PRIMARY KEY (booking_ticket_id)
); -- Tới đây

------------------------------------------------

-- THÊM FK + Ràng buộc
-- Bảng Flight
ALTER TABLE Flight
    ADD CONSTRAINT FK_Flight_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

-- Bảng Airport

-- Bảng FlightRoute
ALTER TABLE FlightRoute
    ADD CONSTRAINT FK_FlightRoute_DepartureAirport
    FOREIGN KEY (departure_airport_id)
    REFERENCES Airport(airport_id);

ALTER TABLE FlightRoute
    ADD CONSTRAINT FK_FlightRoute_ArrivalAirport
    FOREIGN KEY (arrival_airport_id)
    REFERENCES Airport(airport_id);

-- Bảng FlightDetail
ALTER TABLE FlightDetail
    ADD CONSTRAINT FK_FlightDetail_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

ALTER TABLE FlightDetail
    ADD CONSTRAINT FK_FlightDetail_TransitAirport
    FOREIGN KEY (transit_airport_id)
    REFERENCES Airport(airport_id);

-- Bảng HANGVE

-- Bảng TicketClassStatistics 
ALTER TABLE TicketClassStatistics
    ADD CONSTRAINT FK_TicketClassStatistics_Flight
    FOREIGN KEY (flight_id)
    REFERENCES Flight(flight_id);

ALTER TABLE TicketClassStatistics
    ADD CONSTRAINT FK_TicketClassStatistics_TicketClass
    FOREIGN KEY (ticket_class_id)
    REFERENCES TicketClass(ticket_class_id);

-- Bảng DONGIA
ALTER TABLE TicketPrice
    ADD CONSTRAINT FK_TicketPrice_FlightRoute
    FOREIGN KEY (flight_route_id)
    REFERENCES FlightRoute(flight_route_id);

ALTER TABLE TicketPrice
    ADD CONSTRAINT FK_TicketPrice_TicketClass
    FOREIGN KEY (ticket_class_id)
    REFERENCES TicketClass(ticket_class_id);

-- Bảng Employee

-- Bảng Booking_Ticket
ALTER TABLE Booking_Ticket
    ADD CONSTRAINT FK_Booking_Ticket_Flight
    FOREIGN KEY (flight_id)
    REFERENCES Flight(flight_id);

ALTER TABLE Booking_Ticket
    ADD CONSTRAINT FK_Booking_Ticket_TicketClass
    FOREIGN KEY (ticket_class_id)
    REFERENCES TicketClass(ticket_class_id);

ALTER TABLE Booking_Ticket
    ADD CONSTRAINT FK_Booking_Ticket_Employee
    FOREIGN KEY (employee_id)
    REFERENCES Employee(employee_id);

--------------------------------------------
-- Nhập DL
-- Rules
INSERT INTO Rules VALUES (10, 2, 30, 10, 20, 1, 1, 2);

-- Airport
INSERT INTO Airport VALUES 
('SB01', 'Nội Bài', 'Hà Nội'),
('SB02', 'Tân Sơn Nhất', 'TP. HCM'),
('SB03', 'Đà Nẵng', 'Đà Nẵng'),
('SB04', 'Cần Thơ', 'Cần Thơ'),
('SB05', 'Cam Ranh', 'Khánh Hòa'),
('SB06', 'Phú Bài', 'Huế'),
('SB07', 'Liên Khương', 'Lâm Đồng'),
('SB08', 'Vinh', 'Nghệ An'),
('SB09', 'Chu Lai', 'Quảng Nam'),
('SB10', 'Pleiku', 'Gia Lai');



-- FlightRoute (20 tuyến bay từ các sân bay khác nhau)
INSERT INTO FlightRoute VALUES 
('TB01', 'SB01', 'SB02'), ('TB02', 'SB02', 'SB03'), ('TB03', 'SB03', 'SB04'),
('TB04', 'SB04', 'SB05'), ('TB05', 'SB05', 'SB06'), ('TB06', 'SB06', 'SB07'),
('TB07', 'SB07', 'SB08'), ('TB08', 'SB08', 'SB09'), ('TB09', 'SB09', 'SB10'),
('TB10', 'SB10', 'SB01'), ('TB11', 'SB01', 'SB03'), ('TB12', 'SB02', 'SB04'),
('TB13', 'SB03', 'SB05'), ('TB14', 'SB04', 'SB06'), ('TB15', 'SB05', 'SB07'),
('TB16', 'SB06', 'SB08'), ('TB17', 'SB07', 'SB09'), ('TB18', 'SB08', 'SB10'),
('TB19', 'SB09', 'SB01'), ('TB20', 'SB10', 'SB02');



-- Flight
INSERT INTO Flight VALUES 
-- 35 chuyến bay từ 20/6 - 30/6/2025
('CB01', 'TB01', '2025-06-20', '08:00:00', 90, 180),
('CB02', 'TB02', '2025-06-21', '09:00:00', 95, 180),
('CB03', 'TB03', '2025-06-22', '10:00:00', 100, 180),
('CB04', 'TB04', '2025-06-23', '11:00:00', 105, 180),
('CB05', 'TB05', '2025-06-24', '12:00:00', 110, 180),
('CB06', 'TB06', '2025-06-25', '13:00:00', 115, 180),
('CB07', 'TB07', '2025-06-26', '14:00:00', 120, 180),
('CB08', 'TB08', '2025-06-27', '15:00:00', 90, 180),
('CB09', 'TB09', '2025-06-28', '16:00:00', 95, 180),
('CB10', 'TB10', '2025-06-29', '17:00:00', 100, 180),
('CB11', 'TB11', '2025-06-20', '08:30:00', 110, 180),
('CB12', 'TB12', '2025-06-21', '09:30:00', 105, 180),
('CB13', 'TB13', '2025-06-22', '10:30:00', 115, 180),
('CB14', 'TB14', '2025-06-23', '11:30:00', 100, 180),
('CB15', 'TB15', '2025-06-24', '12:30:00', 95, 180),
('CB16', 'TB16', '2025-06-25', '13:30:00', 90, 180),
('CB17', 'TB17', '2025-06-26', '14:30:00', 85, 180),
('CB18', 'TB18', '2025-06-27', '15:30:00', 110, 180),
('CB19', 'TB19', '2025-06-28', '16:30:00', 105, 180),
('CB20', 'TB20', '2025-06-29', '17:30:00', 95, 180),
('CB21', 'TB01', '2025-06-20', '07:00:00', 100, 180),
('CB22', 'TB02', '2025-06-21', '07:15:00', 100, 180),
('CB23', 'TB03', '2025-06-22', '07:30:00', 100, 180),
('CB24', 'TB04', '2025-06-23', '07:45:00', 100, 180),
('CB25', 'TB05', '2025-06-24', '08:00:00', 100, 180),
('CB26', 'TB06', '2025-06-25', '08:15:00', 100, 180),
('CB27', 'TB07', '2025-06-26', '08:30:00', 100, 180),
('CB28', 'TB08', '2025-06-27', '08:45:00', 100, 180),
('CB29', 'TB09', '2025-06-28', '09:00:00', 100, 180),
('CB30', 'TB10', '2025-06-29', '09:15:00', 100, 180),
('CB31', 'TB11', '2025-06-30', '09:30:00', 100, 180),
('CB32', 'TB12', '2025-06-30', '10:00:00', 100, 180),
('CB33', 'TB13', '2025-06-30', '10:30:00', 100, 180),
('CB34', 'TB14', '2025-06-30', '11:00:00', 100, 180),
('CB35', 'TB15', '2025-06-30', '11:30:00', 100, 180),
-- 20 chuyến bay từ 1/6 - 19/6/2025
('CB36', 'TB16', '2025-06-01', '06:00:00', 90, 180),
('CB37', 'TB17', '2025-06-02', '07:00:00', 95, 180),
('CB38', 'TB18', '2025-06-03', '08:00:00', 100, 180),
('CB39', 'TB19', '2025-06-04', '09:00:00', 105, 180),
('CB40', 'TB20', '2025-06-05', '10:00:00', 110, 180),
('CB41', 'TB01', '2025-06-06', '11:00:00', 115, 180),
('CB42', 'TB02', '2025-06-07', '12:00:00', 120, 180),
('CB43', 'TB03', '2025-06-08', '13:00:00', 90, 180),
('CB44', 'TB04', '2025-06-09', '14:00:00', 95, 180),
('CB45', 'TB05', '2025-06-10', '15:00:00', 100, 180),
('CB46', 'TB06', '2025-06-11', '16:00:00', 105, 180),
('CB47', 'TB07', '2025-06-12', '17:00:00', 110, 180),
('CB48', 'TB08', '2025-06-13', '18:00:00', 115, 180),
('CB49', 'TB09', '2025-06-14', '19:00:00', 120, 180),
('CB50', 'TB10', '2025-06-15', '20:00:00', 90, 180),
('CB51', 'TB11', '2025-06-16', '21:00:00', 95, 180),
('CB52', 'TB12', '2025-06-17', '22:00:00', 100, 180),
('CB53', 'TB13', '2025-06-18', '23:00:00', 105, 180),
('CB54', 'TB14', '2025-06-19', '07:00:00', 110, 180),
('CB55', 'TB15', '2025-06-19', '08:00:00', 115, 180),
-- Tháng 1 – 5/2025 (25 chuyến)
('CB56', 'TB16', '2025-01-10', '08:00:00', 100, 180),
('CB57', 'TB17', '2025-01-15', '10:00:00', 100, 180),
('CB58', 'TB18', '2025-01-20', '12:00:00', 100, 180),
('CB59', 'TB19', '2025-01-25', '14:00:00', 100, 180),
('CB60', 'TB20', '2025-01-30', '16:00:00', 100, 180),
('CB61', 'TB01', '2025-02-10', '08:00:00', 100, 180),
('CB62', 'TB02', '2025-02-15', '10:00:00', 100, 180),
('CB63', 'TB03', '2025-02-20', '12:00:00', 100, 180),
('CB64', 'TB04', '2025-02-25', '14:00:00', 100, 180),
('CB65', 'TB05', '2025-02-28', '16:00:00', 100, 180),
('CB66', 'TB06', '2025-03-05', '08:00:00', 100, 180),
('CB67', 'TB07', '2025-03-10', '10:00:00', 100, 180),
('CB68', 'TB08', '2025-03-15', '12:00:00', 100, 180),
('CB69', 'TB09', '2025-03-20', '14:00:00', 100, 180),
('CB70', 'TB10', '2025-03-25', '16:00:00', 100, 180),
('CB71', 'TB11', '2025-04-05', '08:00:00', 100, 180),
('CB72', 'TB12', '2025-04-10', '10:00:00', 100, 180),
('CB73', 'TB13', '2025-04-15', '12:00:00', 100, 180),
('CB74', 'TB14', '2025-04-20', '14:00:00', 100, 180),
('CB75', 'TB15', '2025-04-25', '16:00:00', 100, 180),
('CB76', 'TB16', '2025-05-01', '08:00:00', 100, 180),
('CB77', 'TB17', '2025-05-05', '10:00:00', 100, 180),
('CB78', 'TB18', '2025-05-10', '12:00:00', 100, 180),
('CB79', 'TB19', '2025-05-15', '14:00:00', 100, 180),
('CB80', 'TB20', '2025-05-20', '16:00:00', 100, 180),
-- 20 chuyến bay năm 2024
('CB81', 'TB01', '2024-01-10', '08:00:00', 100, 180),
('CB82', 'TB02', '2024-02-15', '10:00:00', 100, 180),
('CB83', 'TB03', '2024-03-20', '12:00:00', 100, 180),
('CB84', 'TB04', '2024-04-25', '14:00:00', 100, 180),
('CB85', 'TB05', '2024-05-30', '16:00:00', 100, 180),
('CB86', 'TB06', '2024-06-05', '08:00:00', 100, 180),
('CB87', 'TB07', '2024-07-10', '10:00:00', 100, 180),
('CB88', 'TB08', '2024-08-15', '12:00:00', 100, 180),
('CB89', 'TB09', '2024-09-20', '14:00:00', 100, 180),
('CB90', 'TB10', '2024-10-25', '16:00:00', 100, 180),
('CB91', 'TB11', '2024-11-10', '08:00:00', 100, 180),
('CB92', 'TB12', '2024-12-15', '10:00:00', 100, 180),
('CB93', 'TB13', '2024-01-20', '12:00:00', 100, 180),
('CB94', 'TB14', '2024-02-25', '14:00:00', 100, 180),
('CB95', 'TB15', '2024-03-30', '16:00:00', 100, 180),
('CB96', 'TB16', '2024-04-05', '08:00:00', 100, 180),
('CB97', 'TB17', '2024-05-10', '10:00:00', 100, 180),
('CB98', 'TB18', '2024-06-15', '12:00:00', 100, 180),
('CB99', 'TB19', '2024-07-20', '14:00:00', 100, 180),
('CB100', 'TB20', '2024-08-25', '16:00:00', 100, 180),
-- 20 chuyến bay năm 2023
('CB101', 'TB01', '2023-01-05', '08:00:00', 100, 180),
('CB102', 'TB02', '2023-02-10', '10:00:00', 100, 180),
('CB103', 'TB03', '2023-03-15', '12:00:00', 100, 180),
('CB104', 'TB04', '2023-04-20', '14:00:00', 100, 180),
('CB105', 'TB05', '2023-05-25', '16:00:00', 100, 180),
('CB106', 'TB06', '2023-06-30', '08:00:00', 100, 180),
('CB107', 'TB07', '2023-07-05', '10:00:00', 100, 180),
('CB108', 'TB08', '2023-08-10', '12:00:00', 100, 180),
('CB109', 'TB09', '2023-09-15', '14:00:00', 100, 180),
('CB110', 'TB10', '2023-10-20', '16:00:00', 100, 180),
('CB111', 'TB11', '2023-11-25', '08:00:00', 100, 180),
('CB112', 'TB12', '2023-12-30', '10:00:00', 100, 180),
('CB113', 'TB13', '2023-03-01', '08:00:00', 100, 180),
('CB114', 'TB14', '2023-05-01', '10:00:00', 100, 180),
('CB115', 'TB15', '2023-07-01', '12:00:00', 100, 180),
('CB116', 'TB16', '2023-09-01', '14:00:00', 100, 180),
('CB117', 'TB17', '2023-11-01', '16:00:00', 100, 180),
('CB118', 'TB18', '2023-01-15', '08:00:00', 100, 180),
('CB119', 'TB19', '2023-04-15', '10:00:00', 100, 180),
('CB120', 'TB20', '2023-08-15', '12:00:00', 100, 180);



-- FlightDetail
INSERT INTO FlightDetail VALUES 
('CTCB01', 'TB01', 'SB03', 15, 'Dừng nạp nhiên liệu'),
('CTCB02', 'TB02', 'SB04', 20, 'Dừng kỹ thuật'),
('CTCB03', 'TB03', 'SB05', 10, 'Dừng ăn trưa'),
('CTCB04', 'TB04', 'SB06', 15, ''),
('CTCB05', 'TB05', 'SB07', 10, ''),
('CTCB06', 'TB06', 'SB08', 20, ''),
('CTCB07', 'TB07', 'SB09', 15, ''),
('CTCB08', 'TB08', 'SB10', 10, ''),
('CTCB09', 'TB09', 'SB01', 10, ''),
('CTCB10', 'TB10', 'SB02', 20, ''),
('CTCB11', 'TB11', 'SB08', 10, 'Dừng kỹ thuật'),
('CTCB12', 'TB11', 'SB06', 15, 'Dừng ăn trưa'),
('CTCB13', 'TB12', 'SB09', 20, ''),
('CTCB14', 'TB12', 'SB10', 10, 'Dừng nạp nhiên liệu'),
('CTCB15', 'TB13', 'SB01', 15, ''),
('CTCB16', 'TB13', 'SB02', 15, 'Dừng kỹ thuật'),
('CTCB17', 'TB14', 'SB07', 10, ''),
('CTCB18', 'TB14', 'SB08', 15, 'Dừng ăn tối'),
('CTCB19', 'TB15', 'SB09', 10, ''),
('CTCB20', 'TB15', 'SB03', 20, 'Dừng kỹ thuật');



-- TicketClass
INSERT INTO TicketClass VALUES 
('HV01', 'Phổ thông'),
('HV02', 'Thương gia'),
('HV03', 'Hạng nhất'),
('HV04', 'Cao cấp');



-- TicketClassStatistics
INSERT INTO TicketClassStatistics VALUES 
-------- 35 chuyến bay từ 20/6 - 30/6/2025
-- CB01 (TB01 - HV01, HV02)
('TK01', 'CB01', 'HV01', 90, 87, 3), 
('TK02', 'CB01', 'HV02', 90, 89, 1),
-- CB02 (TB02 - HV02, HV03)
('TK03', 'CB02', 'HV02', 90, 88, 2), 
('TK04', 'CB02', 'HV03', 90, 89, 1),
-- CB03 (TB03 - HV01)
('TK05', 'CB03', 'HV01', 180, 178, 2),
-- CB04 (TB04 - HV01, HV02)
('TK06', 'CB04', 'HV01', 90, 90, 0), 
('TK07', 'CB04', 'HV02', 90, 88, 2),
-- CB05 (TB05 - HV03)
('TK08', 'CB05', 'HV03', 180, 179, 1),
-- CB06 (TB06 - HV01, HV04)
('TK09', 'CB06', 'HV01', 90, 88, 2), 
('TK10', 'CB06', 'HV04', 90, 87, 3),
-- CB07 (TB07 - HV02)
('TK11', 'CB07', 'HV02', 180, 178, 2),
-- CB08 (TB08 - HV02, HV03)
('TK12', 'CB08', 'HV02', 90, 87, 3), 
('TK13', 'CB08', 'HV03', 90, 90, 0),
-- CB09 (TB09 - HV01, HV02)
('TK14', 'CB09', 'HV01', 90, 87, 3), 
('TK15', 'CB09', 'HV02', 90, 89, 1),
-- CB10 (TB10 - HV01, HV03)
('TK16', 'CB10', 'HV01', 90, 88, 2), 
('TK17', 'CB10', 'HV03', 90, 89, 1),
-- CB11 (TB11 - HV01)
('TK18', 'CB11', 'HV01', 180, 177, 3), 
-- CB12 (TB12 - HV01, HV02)
('TK19', 'CB12', 'HV01', 90, 88, 2), 
('TK20', 'CB12', 'HV02', 90, 89, 1),
-- CB13 (TB13 - HV02, HV03)
('TK21', 'CB13', 'HV02', 90, 87, 3), 
('TK22', 'CB13', 'HV03', 90, 89, 1),
-- CB14 (TB14 - HV03)
('TK23', 'CB14', 'HV03', 180, 179, 1),
-- CB15 (TB15 - HV01)
('TK24', 'CB15', 'HV01', 180, 177, 3),
-- CB16 (TB16 - HV02, HV04)
('TK25', 'CB16', 'HV02', 90, 90, 0), 
('TK26', 'CB16', 'HV04', 90, 88, 2),
-- CB17 (TB17 - HV01)
('TK27', 'CB17', 'HV01', 180, 179, 1),
-- CB18 (TB18 - HV02, HV03)
('TK28', 'CB18', 'HV02', 90, 89, 1), 
('TK29', 'CB18', 'HV03', 90, 87, 3),
-- CB19 (TB19 - HV02)
('TK30', 'CB19', 'HV02', 180, 178, 2),
-- CB20 (TB20 - HV01, HV03) - Bỏ HV01
('TK31', 'CB20', 'HV03', 180, 177, 3),
-- CB21 (TB01 - HV01, HV02) – đủ 2 hạng
('TK32', 'CB21', 'HV01', 90, 87, 3),
('TK33', 'CB21', 'HV02', 90, 90, 0),
-- CB22 (TB02 - HV02, HV03) – đủ 2 hạng
('TK34', 'CB22', 'HV02', 90, 89, 1),
('TK35', 'CB22', 'HV03', 90, 88, 2),
-- CB23 (TB03 - HV01) – chỉ 1 hạng
('TK36', 'CB23', 'HV01', 180, 178, 2),
-- CB24 (TB04 - HV01, HV02) – đủ 2 hạng
('TK37', 'CB24', 'HV01', 90, 90, 0),
('TK38', 'CB24', 'HV02', 90, 89, 1),
-- CB25 (TB05 - HV03) – chỉ 1 hạng
('TK39', 'CB25', 'HV03', 180, 177, 3),
-- CB26 (TB06 - HV01, HV04) – đủ 2 hạng
('TK40', 'CB26', 'HV01', 90, 87, 3),
('TK41', 'CB26', 'HV04', 90, 90, 0),
-- CB27 (TB07 - HV02) – chỉ 1 hạng
('TK42', 'CB27', 'HV02', 180, 178, 2),
-- CB28 (TB08 - HV02, HV03) – đủ 2 hạng
('TK43', 'CB28', 'HV02', 90, 88, 2),
('TK44', 'CB28', 'HV03', 90, 89, 1),
-- CB29 (TB09 - HV01, HV02) – đủ 2 hạng
('TK45', 'CB29', 'HV01', 90, 90, 0),
('TK46', 'CB29', 'HV02', 90, 88, 2),
-- CB30 (TB10 - HV01, HV03) – đủ 2 hạng
('TK47', 'CB30', 'HV01', 90, 87, 3),
('TK48', 'CB30', 'HV03', 90, 90, 0),
-- CB31 (TB11 - HV01) – chỉ 1 hạng
('TK49', 'CB31', 'HV01', 180, 178, 2),
-- CB32 (TB12 - HV01, HV02) – skip HV02
('TK50', 'CB32', 'HV01', 180, 179, 1),
-- CB33 (TB13 - HV02, HV03) – skip HV03
('TK51', 'CB33', 'HV02', 180, 177, 3),
-- CB34 (TB14 - HV03) – chỉ 1 hạng
('TK52', 'CB34', 'HV03', 180, 179, 1),
-- CB35 (TB15 - HV01) – chỉ 1 hạng
('TK53', 'CB35', 'HV01', 180, 178, 2),


-------- 20 chuyến bay từ 1/6 - 19/6/2025 
-- CB36 (TB16 - HV02, HV04) – đủ 2 hạng
('TK54', 'CB36', 'HV02', 100, 98, 2),
('TK55', 'CB36', 'HV04', 80, 78, 2),
-- CB37 (TB17 - HV01) – chỉ 1 hạng
('TK56', 'CB37', 'HV01', 180, 177, 3),
-- CB38 (TB18 - HV02, HV03) – đủ 2 hạng
('TK57', 'CB38', 'HV02', 100, 98, 2),
('TK58', 'CB38', 'HV03', 80, 78, 2),
-- CB39 (TB19 - HV02) – chỉ 1 hạng
('TK59', 'CB39', 'HV02', 180, 177, 3),
-- CB40 (TB20 - HV01, HV03) – đủ 2 hạng
('TK60', 'CB40', 'HV01', 110, 108, 2),
('TK61', 'CB40', 'HV03', 70, 69, 1),
-- CB41 (TB01 - HV01, HV02) – đủ 2 hạng
('TK62', 'CB41', 'HV01', 90, 88, 2),
('TK63', 'CB41', 'HV02', 90, 89, 1),
-- CB42 (TB02 - HV02, HV03) – bỏ HV03
('TK64', 'CB42', 'HV02', 180, 177, 3),
-- CB43 (TB03 - HV01) – chỉ 1 hạng
('TK65', 'CB43', 'HV01', 180, 179, 1),
-- CB44 (TB04 - HV01, HV02) – đủ 2 hạng
('TK66', 'CB44', 'HV01', 100, 98, 2),
('TK67', 'CB44', 'HV02', 80, 78, 2),
-- CB45 (TB05 - HV03) – chỉ 1 hạng
('TK68', 'CB45', 'HV03', 180, 178, 2),
-- CB46 (TB06 - HV01, HV04) – đủ 2 hạng
('TK69', 'CB46', 'HV01', 90, 88, 2),
('TK70', 'CB46', 'HV04', 90, 89, 1),
-- CB47 (TB07 - HV02) – chỉ 1 hạng
('TK71', 'CB47', 'HV02', 180, 178, 2),
-- CB48 (TB08 - HV02, HV03) – đủ 2 hạng
('TK72', 'CB48', 'HV02', 115, 113, 2),
('TK73', 'CB48', 'HV03', 65, 63, 2),
-- CB49 (TB09 - HV01, HV02) – đủ 2 hạng
('TK74', 'CB49', 'HV01', 120, 117, 3),
('TK75', 'CB49', 'HV02', 60, 59, 1),
-- CB50 (TB10 - HV01, HV03) – đủ 2 hạng
('TK76', 'CB50', 'HV01', 100, 97, 3),
('TK77', 'CB50', 'HV03', 80, 78, 2),
-- CB51 (TB11 - HV01) – chỉ 1 hạng
('TK78', 'CB51', 'HV01', 180, 177, 3),
-- CB52 (TB12 - HV01, HV02) – đủ 2 hạng
('TK79', 'CB52', 'HV01', 100, 97, 3),
('TK80', 'CB52', 'HV02', 80, 78, 2),
-- CB53 (TB13 - HV02, HV03) – đủ 2 hạng
('TK81', 'CB53', 'HV02', 105, 104, 1),
('TK82', 'CB53', 'HV03', 75, 74, 1),
-- CB54 (TB14 - HV03) – chỉ 1 hạng
('TK83', 'CB54', 'HV03', 180, 179, 1),
-- CB55 (TB15 - HV01) – chỉ 1 hạng
('TK84', 'CB55', 'HV01', 180, 178, 2),


--------- Tháng 1 – 5/2025 (25 chuyến)
-- CB56 (TB16 - HV02, HV04) – đủ 2 hạng
('TK85', 'CB56', 'HV02', 90, 88, 2),
('TK86', 'CB56', 'HV04', 90, 89, 1),
-- CB57 (TB17 - HV01) – chỉ 1 hạng
('TK87', 'CB57', 'HV01', 180, 177, 3),
-- CB58 (TB18 - HV02, HV03) – đủ 2 hạng
('TK88', 'CB58', 'HV02', 100, 97, 3),
('TK89', 'CB58', 'HV03', 80, 80, 0),
-- CB59 (TB19 - HV02) – chỉ 1 hạng
('TK90', 'CB59', 'HV02', 180, 179, 1),
-- CB60 (TB20 - HV01, HV03) – đủ 2 hạng
('TK91', 'CB60', 'HV01', 100, 100, 0),
('TK92', 'CB60', 'HV03', 80, 78, 2),
-- CB61 (TB01 - HV01, HV02) – đủ 2 hạng
('TK93', 'CB61', 'HV01', 90, 88, 2),
('TK94', 'CB61', 'HV02', 90, 90, 0),
-- CB62 (TB02 - HV03, HV02) – đủ 2 hạng
('TK95', 'CB62', 'HV03', 100, 99, 1),
('TK96', 'CB62', 'HV02', 80, 80, 0),
-- CB63 (TB03 - HV01) – chỉ 1 hạng
('TK97', 'CB63', 'HV01', 180, 178, 2),
-- CB64 (TB04 - HV01, HV02) – đủ 2 hạng
('TK98', 'CB64', 'HV01', 100, 100, 0),
('TK99', 'CB64', 'HV02', 80, 78, 2),
-- CB65 (TB05 - HV03) – chỉ 1 hạng
('TK100', 'CB65', 'HV03', 180, 179, 1),
-- CB66 (TB06 - HV01, HV04) – đủ 2 hạng
('TK101', 'CB66', 'HV01', 90, 88, 2),
('TK102', 'CB66', 'HV04', 90, 88, 2),
-- CB67 (TB07 - HV02) – chỉ 1 hạng
('TK103', 'CB67', 'HV02', 180, 177, 3),
-- CB68 (TB08 - HV02, HV03) – đủ 2 hạng
('TK104', 'CB68', 'HV02', 100, 98, 2),
('TK105', 'CB68', 'HV03', 80, 78, 2),
-- CB69 (TB09 - HV01, HV02) – đủ 2 hạng
('TK106', 'CB69', 'HV01', 100, 98, 2),
('TK107', 'CB69', 'HV02', 80, 78, 2),
-- CB70 (TB10 - HV03, HV01) – đủ 2 hạng
('TK108', 'CB70', 'HV03', 100, 98, 2),
('TK109', 'CB70', 'HV01', 80, 79, 1),
-- CB71 (TB11 - HV01) – chỉ 1 hạng
('TK110', 'CB71', 'HV01', 180, 178, 2),
-- CB72 (TB12 - HV01, HV02) – đủ 2 hạng
('TK111', 'CB72', 'HV01', 100, 100, 0),
('TK112', 'CB72', 'HV02', 80, 78, 2),
-- CB73 (TB13 - HV02, HV03) – đủ 2 hạng
('TK113', 'CB73', 'HV02', 90, 89, 1),
('TK114', 'CB73', 'HV03', 90, 90, 0),
-- CB74 (TB14 - HV03) – chỉ 1 hạng
('TK115', 'CB74', 'HV03', 180, 180, 0),
-- CB75 (TB15 - HV01) – chỉ 1 hạng
('TK116', 'CB75', 'HV01', 180, 178, 2),
-- CB76 (TB16 - HV02, HV04) – đủ 2 hạng
('TK117', 'CB76', 'HV02', 100, 99, 1),
('TK118', 'CB76', 'HV04', 80, 80, 0),
-- CB77 (TB17 - HV01) – chỉ 1 hạng
('TK119', 'CB77', 'HV01', 180, 180, 0),
-- CB78 (TB18 - HV03, HV02) – đủ 2 hạng
('TK120', 'CB78', 'HV03', 100, 98, 2),
('TK121', 'CB78', 'HV02', 80, 78, 2),
-- CB79 (TB19 - HV02) – chỉ 1 hạng
('TK122', 'CB79', 'HV02', 180, 178, 2),
-- CB80 (TB20 - HV03, HV01) – đủ 2 hạng
('TK123', 'CB80', 'HV03', 100, 98, 2),
('TK124', 'CB80', 'HV01', 80, 78, 2),


-------- 20 chuyến bay năm 2024
-- CB81 (TB01 - HV01, HV02)
('TK125', 'CB81', 'HV01', 90, 88, 2), 
('TK126', 'CB81', 'HV02', 90, 89, 1),
-- CB82 (TB02 - HV02, HV03)
('TK127', 'CB82', 'HV02', 180, 178, 2),
-- CB83 (TB03 - HV01)
('TK128', 'CB83', 'HV01', 180, 179, 1),
-- CB84 (TB04 - HV01, HV02)
('TK129', 'CB84', 'HV01', 100, 97, 3), 
('TK130', 'CB84', 'HV02', 80, 78, 2),
-- CB85 (TB05 - HV03)
('TK131', 'CB85', 'HV03', 180, 178, 2),
-- CB86 (TB06 - HV01, HV04) - Bỏ HV01
('TK132', 'CB86', 'HV04', 180, 178, 2),
-- CB87 (TB07 - HV02)
('TK133', 'CB87', 'HV02', 180, 179, 1),
-- CB88 (TB08 - HV02, HV03)
('TK134', 'CB88', 'HV02', 100, 100, 0), 
('TK135', 'CB88', 'HV03', 80, 78, 2),
-- CB89 (TB09 - HV01, HV02) - Bỏ HV01
('TK136', 'CB89', 'HV02', 180, 177, 3),
-- CB90 (TB10 - HV01, HV03)
('TK137', 'CB90', 'HV01', 100, 98, 2), 
('TK138', 'CB90', 'HV03', 80, 80, 0),
-- CB91 (TB11 - HV01)
('TK139', 'CB91', 'HV01', 180, 178, 2),
-- CB92 (TB12 - HV01, HV02)
('TK140', 'CB92', 'HV01', 120, 119, 1), 
('TK141', 'CB92', 'HV02', 60, 60, 0),
-- CB93 (TB13 - HV02, HV03) - Bỏ HV02
('TK142', 'CB93', 'HV03', 180, 178, 2),
-- CB94 (TB14 - HV03)
('TK143', 'CB94', 'HV03', 180, 177, 3),
-- CB95 (TB15 - HV01)
('TK144', 'CB95', 'HV01', 180, 178, 2),
-- CB96 (TB16 - HV02, HV04)
('TK145', 'CB96', 'HV02', 90, 90, 0),
('TK146', 'CB96', 'HV04', 90, 88, 2),
-- CB97 (TB17 - HV01)
('TK147', 'CB97', 'HV01', 180, 178, 2),
-- CB98 (TB18 - HV02, HV03)
('TK148', 'CB98', 'HV02', 100, 97, 3), 
('TK149', 'CB98', 'HV03', 80, 80, 0),
-- CB99 (TB19 - HV02)
('TK150', 'CB99', 'HV02', 180, 178, 2),
-- CB100 (TB20 - HV01, HV03) – Bỏ HV03
('TK151', 'CB100', 'HV01', 180, 179, 1),

-------- 20 chuyến bay năm 2023
-- CB101 (TB01 - HV01, HV02)
('TK152', 'CB101', 'HV01', 90, 88, 2),
('TK153', 'CB101', 'HV02', 90, 87, 3),
-- CB102 (TB02 - HV02, HV03) – Bỏ HV03
('TK154', 'CB102', 'HV02', 180, 179, 1),
-- CB103 (TB03 - HV01)
('TK155', 'CB103', 'HV01', 180, 177, 3),
-- CB104 (TB04 - HV01, HV02) – đủ
('TK156', 'CB104', 'HV01', 100, 98, 2),
('TK157', 'CB104', 'HV02', 80, 78, 2),
-- CB105 (TB05 - HV03)
('TK158', 'CB105', 'HV03', 180, 180, 0),
-- CB106 (TB06 - HV01, HV04) – thiếu 1 hạng
('TK159', 'CB106', 'HV01', 180, 178, 2),
-- CB107 (TB07 - HV02)
('TK160', 'CB107', 'HV02', 180, 179, 1),
-- CB108 (TB08 - HV02, HV03) – đủ
('TK161', 'CB108', 'HV02', 100, 98, 2),
('TK162', 'CB108', 'HV03', 80, 77, 3),
-- CB109 (TB09 - HV01, HV02) – đủ
('TK163', 'CB109', 'HV01', 90, 90, 0),
('TK164', 'CB109', 'HV02', 90, 88, 2),
-- CB110 (TB10 - HV01, HV03) – Bỏ HV01
('TK165', 'CB110', 'HV03', 180, 178, 2),
-- CB111 (TB11 - HV01)
('TK166', 'CB111', 'HV01', 180, 177, 3),
-- CB112 (TB12 - HV01, HV02) – đủ
('TK167', 'CB112', 'HV01', 120, 118, 2),
('TK168', 'CB112', 'HV02', 60, 57, 3),
-- CB113 (TB13 - HV02, HV03) – đủ
('TK169', 'CB113', 'HV02', 90, 87, 3),
('TK170', 'CB113', 'HV03', 90, 89, 1),
-- CB114 (TB14 - HV03)
('TK171', 'CB114', 'HV03', 180, 178, 2),
-- CB115 (TB15 - HV01)
('TK172', 'CB115', 'HV01', 180, 180, 0),
-- CB116 (TB16 - HV02, HV04) – đủ
('TK173', 'CB116', 'HV02', 100, 97, 3),
('TK174', 'CB116', 'HV04', 80, 78, 2),
-- CB117 (TB17 - HV01)
('TK175', 'CB117', 'HV01', 180, 177, 3),
-- CB118 (TB18 - HV02, HV03) – đủ
('TK176', 'CB118', 'HV02', 100, 98, 2),
('TK177', 'CB118', 'HV03', 80, 79, 1),
-- CB119 (TB19 - HV02)
('TK178', 'CB119', 'HV02', 180, 180, 0),
-- CB120 (TB20 - HV01, HV03) – Bỏ HV03
('TK179', 'CB120', 'HV01', 180, 178, 2);



-- TicketPrice (30 dòng: 10 tuyến bay có 1 hạng vé, 20 tuyến có 2 hạng vé)
INSERT INTO TicketPrice VALUES
-- TB01 (2 hạng)
('DG01', 'TB01', 'HV01', 1000000), 
('DG02', 'TB01', 'HV02', 1500000),
-- TB02 (2 hạng)
('DG03', 'TB02', 'HV02', 1300000), 
('DG04', 'TB02', 'HV03', 1800000),
-- TB03 (1 hạng)
('DG05', 'TB03', 'HV01', 1100000),
-- TB04 (2 hạng)
('DG06', 'TB04', 'HV01', 1200000), 
('DG07', 'TB04', 'HV02', 1700000),
-- TB05 (1 hạng)
('DG08', 'TB05', 'HV03', 1900000),
-- TB06 (2 hạng)
('DG09', 'TB06', 'HV01', 1150000), 
('DG10', 'TB06', 'HV04', 2500000),
-- TB07 (1 hạng)
('DG11', 'TB07', 'HV02', 1350000),
-- TB08 (2 hạng)
('DG12', 'TB08', 'HV02', 1400000), 
('DG13', 'TB08', 'HV03', 1950000),
-- TB09 (2 hạng)
('DG14', 'TB09', 'HV01', 1000000), 
('DG15', 'TB09', 'HV02', 1450000),
-- TB10 (2 hạng)
('DG16', 'TB10', 'HV01', 1050000), 
('DG17', 'TB10', 'HV03', 1750000),
-- TB11 (1 hạng)
('DG18', 'TB11', 'HV01', 950000),
-- TB12 (2 hạng)
('DG19', 'TB12', 'HV01', 1100000), 
('DG20', 'TB12', 'HV02', 1600000),
-- TB13 (2 hạng)
('DG21', 'TB13', 'HV02', 1400000), 
('DG22', 'TB13', 'HV03', 2000000),
-- TB14 (1 hạng)
('DG23', 'TB14', 'HV03', 2100000),
-- TB15 (1 hạng)
('DG24', 'TB15', 'HV01', 1200000),
-- TB16 (2 hạng)
('DG25', 'TB16', 'HV02', 1500000), 
('DG26', 'TB16', 'HV04', 2400000),
-- TB17 (1 hạng)
('DG27', 'TB17', 'HV01', 1000000),
-- TB18 (2 hạng)
('DG28', 'TB18', 'HV02', 1350000), 
('DG29', 'TB18', 'HV03', 1850000),
-- TB19 (1 hạng)
('DG30', 'TB19', 'HV02', 1300000),
-- TB20 (2 hạng)
('DG31', 'TB20', 'HV01', 1350000), 
('DG32', 'TB20', 'HV03', 1850000);


-- Employee
INSERT INTO Employee VALUES 
('NV01', 'admin1', 'pass1', 'Nguyễn Văn A', '123456789', 'Nam', '0909000001', '2025-01-01'),
('NV02', 'admin2', 'pass2', 'Trần Thị B', '123456788', 'Nữ', '0909000002', '2025-01-02'),
('NV03', 'admin3', 'pass3', 'Lê Văn C', '123456787', 'Nam', '0909000003', '2025-01-03'),
('NV04', 'admin4', 'pass4', 'Phạm Thị D', '123456786', 'Nữ', '0909000004', '2025-01-04'),
('NV05', 'admin5', 'pass5', 'Hoàng Văn E', '123456785', 'Nam', '0909000005', '2025-01-05');

-- Booking_Ticket
INSERT INTO Booking_Ticket VALUES
-------- 35 chuyến bay từ 20/6 - 30/6/2025
('PDC01', 'CB01', 'Lê Thị A', '259142893', 'Nữ', '0958895682', 'HV01', 1000000, '2025-06-18', FALSE, 'NV01'),
('PDC02', 'CB01', 'Phan Ngọc', '970430275', 'Nữ', '0950935764', 'HV01', 1000000, '2025-06-18', FALSE, 'NV03'),
('PDC03', 'CB01', 'Hoàng Mai', '696719126', 'Nữ', '0949679121', 'HV01', 1000000, '2025-06-18', TRUE, 'NV02'),
('PDC04', 'CB01', 'Phan Bích', '914820005', 'Nữ', '0999946940', 'HV02', 1500000, '2025-06-18', FALSE, 'NV03'),
('PDC05', 'CB02', 'Lê Linh', '646930224', 'Nữ', '0922213753', 'HV02', 1300000, '2025-06-19', TRUE, 'NV05'),
('PDC06', 'CB02', 'Trần Diệu', '022831402', 'Nữ', '0916454623', 'HV02', 1300000, '2025-06-19', FALSE, 'NV02'),
('PDC07', 'CB02', 'Võ Hằng', '106494565', 'Nữ', '0917808873', 'HV03', 1800000, '2025-06-19', FALSE, 'NV02'),
('PDC08', 'CB03', 'Nguyễn Văn Giang', '117382178', 'Nam', '0905400573', 'HV01', 1100000, '2025-06-20', FALSE, 'NV02'),
('PDC09', 'CB03', 'Võ Hải', '857927737', 'Nam', '0968797335', 'HV01', 1100000, '2025-06-20', TRUE, 'NV02'),
('PDC10', 'CB04', 'Trần Khánh', '476347219', 'Nam', '0989737259', 'HV02', 1700000, '2025-06-21', TRUE, 'NV03'),
('PDC11', 'CB04', 'Phan Diệu', '847831663', 'Nữ', '0957477508', 'HV02', 1700000, '2025-06-21', TRUE, 'NV03'),
('PDC12', 'CB05', 'Trần Cảnh', '339097421', 'Nam', '0975200704', 'HV03', 1900000, '2025-06-22', TRUE, 'NV04'),
('PDC13', 'CB06', 'Phạm Dũng', '568297102', 'Nam', '0939549498', 'HV01', 1150000, '2025-06-23', TRUE, 'NV02'),
('PDC14', 'CB06', 'Trần Bình', '268368080', 'Nam', '0991818646', 'HV01', 1150000, '2025-06-23', TRUE, 'NV05'),
('PDC15', 'CB06', 'Võ Khánh', '237678263', 'Nam', '0943512772', 'HV04', 2500000, '2025-06-23', TRUE, 'NV03'),
('PDC16', 'CB06', 'Phan Minh', '631382428', 'Nam', '0959534086', 'HV04', 2500000, '2025-06-23', TRUE, 'NV05'),
('PDC17', 'CB06', 'Huỳnh Ngọc', '953658497', 'Nữ', '0914218209', 'HV04', 2500000, '2025-06-23', TRUE, 'NV03'),
('PDC18', 'CB07', 'Trần Minh', '854688682', 'Nam', '0995087414', 'HV02', 1350000, '2025-06-24', TRUE, 'NV02'),
('PDC19', 'CB07', 'Phan Bình', '660904124', 'Nam', '0997545733', 'HV02', 1350000, '2025-06-24', TRUE, 'NV04'),
('PDC20', 'CB08', 'Hoàng Hằng', '918822137', 'Nữ', '0983205337', 'HV02', 1400000, '2025-06-25', TRUE, 'NV01'),
('PDC21', 'CB08', 'Lê Dũng', '087914319', 'Nam', '0990092768', 'HV02', 1400000, '2025-06-25', TRUE, 'NV05'),
('PDC22', 'CB08', 'Phạm Bình', '159353896', 'Nam', '0939011507', 'HV02', 1400000, '2025-06-25', TRUE, 'NV01'),
('PDC23', 'CB09', 'Võ Dũng', '467853020', 'Nam', '0982381186', 'HV01', 1000000, '2025-06-26', TRUE, 'NV04'),
('PDC24', 'CB09', 'Phạm Cảnh', '346216990', 'Nam', '0993370273', 'HV01', 1000000, '2025-06-26', FALSE, 'NV02'),
('PDC25', 'CB09', 'Nguyễn Văn Cảnh', '539602596', 'Nam', '0902255108', 'HV01', 1000000, '2025-06-26', FALSE, 'NV04'),
('PDC26', 'CB09', 'Phạm Hằng', '941791587', 'Nữ', '0915351327', 'HV02', 1450000, '2025-06-26', FALSE, 'NV05'),
('PDC27', 'CB10', 'Nguyễn Thị Diệu', '111258065', 'Nữ', '0961490705', 'HV01', 1050000, '2025-06-27', TRUE, 'NV02'),
('PDC28', 'CB10', 'Lê An', '825828090', 'Nam', '0957885024', 'HV01', 1050000, '2025-06-27', FALSE, 'NV02'),
('PDC29', 'CB10', 'Lê Hải', '407114342', 'Nam', '0937868598', 'HV03', 1750000, '2025-06-27', TRUE, 'NV05'),
('PDC30', 'CB11', 'Phan Minh', '072470840', 'Nam', '0910544603', 'HV01', 950000, '2025-06-18', FALSE, 'NV02'),
('PDC31', 'CB11', 'Nguyễn Thị Bích', '538214390', 'Nữ', '0966259669', 'HV01', 950000, '2025-06-18', FALSE, 'NV05'),
('PDC32', 'CB11', 'Phan Cảnh', '813860869', 'Nam', '0918234861', 'HV01', 950000, '2025-06-18', TRUE, 'NV05'),
('PDC33', 'CB12', 'Hoàng Dũng', '226158514', 'Nam', '0937968092', 'HV01', 1100000, '2025-06-19', TRUE, 'NV04'),
('PDC34', 'CB12', 'Phan Bình', '733852816', 'Nam', '0983900519', 'HV01', 1100000, '2025-06-19', TRUE, 'NV05'),
('PDC35', 'CB12', 'Phạm Giang', '357862125', 'Nam', '0910240862', 'HV02', 1600000, '2025-06-19', TRUE, 'NV01'),
('PDC36', 'CB13', 'Lê Cảnh', '490847359', 'Nam', '0908114159', 'HV02', 1400000, '2025-06-20', FALSE, 'NV05'),
('PDC37', 'CB13', 'Phạm Khánh', '564334020', 'Nam', '0956407398', 'HV02', 1400000, '2025-06-20', TRUE, 'NV03'),
('PDC38', 'CB13', 'Hoàng Chi', '122952639', 'Nữ', '0970710131', 'HV02', 1400000, '2025-06-20', FALSE, 'NV03'),
('PDC39', 'CB13', 'Trần Minh', '628915566', 'Nam', '0980431986', 'HV03', 2000000, '2025-06-20', FALSE, 'NV05'),
('PDC40', 'CB14', 'Trần Dũng', '803346782', 'Nam', '0919820829', 'HV03', 2100000, '2025-06-21', FALSE, 'NV04'),
('PDC41', 'CB15', 'Phan Mai', '499865041', 'Nữ', '0905045408', 'HV01', 1200000, '2025-06-22', FALSE, 'NV01'),
('PDC42', 'CB15', 'Trần Hải', '577695646', 'Nam', '0905323205', 'HV01', 1200000, '2025-06-22', TRUE, 'NV02'),
('PDC43', 'CB15', 'Huỳnh Cảnh', '531365135', 'Nam', '0957420041', 'HV01', 1200000, '2025-06-22', FALSE, 'NV01'),
('PDC44', 'CB16', 'Hoàng Bình', '250383649', 'Nam', '0980228825', 'HV04', 2400000, '2025-06-23', TRUE, 'NV05'),
('PDC45', 'CB16', 'Nguyễn Thị Bích', '222103713', 'Nữ', '0969113430', 'HV04', 2400000, '2025-06-23', TRUE, 'NV01'),
('PDC46', 'CB17', 'Trần Mai', '959200298', 'Nữ', '0944799352', 'HV01', 1000000, '2025-06-24', TRUE, 'NV01'),
('PDC47', 'CB18', 'Trần Minh', '351695100', 'Nam', '0936751995', 'HV02', 1350000, '2025-06-25', FALSE, 'NV04'),
('PDC48', 'CB18', 'Huỳnh Minh', '240641389', 'Nam', '0907714116', 'HV03', 1850000, '2025-06-25', FALSE, 'NV05'),
('PDC49', 'CB18', 'Trần Hằng', '546108868', 'Nữ', '0957921426', 'HV03', 1850000, '2025-06-25', TRUE, 'NV05'),
('PDC50', 'CB18', 'Phan Hằng', '116296505', 'Nữ', '0945754870', 'HV03', 1850000, '2025-06-25', FALSE, 'NV01'),
('PDC51', 'CB19', 'Huỳnh Khánh', '291074826', 'Nam', '0999290964', 'HV02', 1300000, '2025-06-26', TRUE, 'NV03'),
('PDC52', 'CB19', 'Nguyễn Văn Bình', '032587338', 'Nam', '0934324041', 'HV02', 1300000, '2025-06-26', FALSE, 'NV04'),
('PDC53', 'CB20', 'Trần Ngọc', '086740937', 'Nữ', '0935426088', 'HV03', 1850000, '2025-06-27', TRUE, 'NV03'),
('PDC54', 'CB20', 'Nguyễn Văn Hải', '449643569', 'Nam', '0970096590', 'HV03', 1850000, '2025-06-27', TRUE, 'NV04'),
('PDC55', 'CB20', 'Võ Anh', '967847662', 'Nữ', '0926347250', 'HV03', 1850000, '2025-06-27', FALSE, 'NV03'),
('PDC56', 'CB21', 'Lê Thị A', '111111111', 'Nữ', '0912340001', 'HV01', 1000000, '2025-06-18', TRUE, 'NV01'),
('PDC57', 'CB21', 'Nguyễn Văn B', '222222222', 'Nam', '0912340002', 'HV01', 1000000, '2025-06-18', FALSE, 'NV03'),
('PDC58', 'CB21', 'Trần Thị C', '333333333', 'Nữ', '0912340003', 'HV01', 1000000, '2025-06-18', TRUE, 'NV05'),
('PDC59', 'CB22', 'Phạm Văn D', '444444444', 'Nam', '0912340004', 'HV02', 1300000, '2025-06-19', TRUE, 'NV02'),
('PDC60', 'CB22', 'Hoàng Thị E', '555555555', 'Nữ', '0912340005', 'HV03', 1800000, '2025-06-19', FALSE, 'NV04'),
('PDC61', 'CB22', 'Vũ Văn F', '666666666', 'Nam', '0912340006', 'HV03', 1800000, '2025-06-19', TRUE, 'NV01'),
('PDC62', 'CB23', 'Đặng Thị G', '777777777', 'Nữ', '0912340007', 'HV01', 1100000, '2025-06-20', FALSE, 'NV03'),
('PDC63', 'CB23', 'Bùi Văn H', '888888888', 'Nam', '0912340008', 'HV01', 1100000, '2025-06-20', TRUE, 'NV05'),
('PDC64', 'CB24', 'Lý Thị I', '999999999', 'Nữ', '0912340009', 'HV02', 1700000, '2025-06-21', TRUE, 'NV02'),
('PDC65', 'CB25', 'Nguyễn Văn K', '010101010', 'Nam', '0912340010', 'HV03', 1900000, '2025-06-22', FALSE, 'NV04'),
('PDC66', 'CB25', 'Trần Thị L', '020202020', 'Nữ', '0912340011', 'HV03', 1900000, '2025-06-22', TRUE, 'NV01'),
('PDC67', 'CB25', 'Phạm Văn M', '030303030', 'Nam', '0912340012', 'HV03', 1900000, '2025-06-22', FALSE, 'NV03'),
('PDC68', 'CB26', 'Hoàng Thị N', '040404040', 'Nữ', '0912340013', 'HV01', 1150000, '2025-06-23', TRUE, 'NV05'),
('PDC69', 'CB26', 'Vũ Văn O', '050505050', 'Nam', '0912340014', 'HV01', 1150000, '2025-06-23', FALSE, 'NV02'),
('PDC70', 'CB26', 'Đặng Thị P', '060606060', 'Nữ', '0912340015', 'HV01', 1150000, '2025-06-23', TRUE, 'NV04'),
('PDC71', 'CB27', 'Bùi Văn Q', '070707070', 'Nam', '0912340016', 'HV02', 1350000, '2025-06-24', FALSE, 'NV01'),
('PDC72', 'CB27', 'Lý Thị R', '080808080', 'Nữ', '0912340017', 'HV02', 1350000, '2025-06-24', TRUE, 'NV03'),
('PDC73', 'CB28', 'Nguyễn Văn S', '090909090', 'Nam', '0912340018', 'HV02', 1400000, '2025-06-25', TRUE, 'NV05'),
('PDC74', 'CB28', 'Trần Thị T', '101010101', 'Nữ', '0912340019', 'HV02', 1400000, '2025-06-25', FALSE, 'NV02'),
('PDC75', 'CB28', 'Phạm Văn U', '111111111', 'Nam', '0912340020', 'HV03', 1950000, '2025-06-25', TRUE, 'NV04'),
('PDC76', 'CB29', 'Hoàng Thị V', '121212121', 'Nữ', '0912340021', 'HV02', 1450000, '2025-06-26', FALSE, 'NV01'),
('PDC77', 'CB29', 'Vũ Văn X', '131313131', 'Nam', '0912340022', 'HV02', 1450000, '2025-06-26', TRUE, 'NV03'),
('PDC78', 'CB30', 'Đặng Thị Y', '141414141', 'Nữ', '0912340023', 'HV01', 1050000, '2025-06-27', TRUE, 'NV05'),
('PDC79', 'CB30', 'Bùi Văn Z', '151515151', 'Nam', '0912340024', 'HV01', 1050000, '2025-06-27', FALSE, 'NV02'),
('PDC80', 'CB30', 'Lý Thị AA', '161616161', 'Nữ', '0912340025', 'HV01', 1050000, '2025-06-27', TRUE, 'NV04'),
('PDC81', 'CB31', 'Nguyễn Văn BB', '171717171', 'Nam', '0912340026', 'HV01', 950000, '2025-06-28', FALSE, 'NV01'),
('PDC82', 'CB31', 'Trần Thị CC', '181818181', 'Nữ', '0912340027', 'HV01', 950000, '2025-06-28', TRUE, 'NV03'),
('PDC83', 'CB32', 'Phạm Văn DD', '191919191', 'Nam', '0912340028', 'HV01', 1100000, '2025-06-28', TRUE, 'NV05'),
('PDC84', 'CB33', 'Hoàng Thị EE', '202020202', 'Nữ', '0912340029', 'HV02', 1400000, '2025-06-28', FALSE, 'NV02'),
('PDC85', 'CB33', 'Vũ Văn FF', '212121212', 'Nam', '0912340030', 'HV02', 1400000, '2025-06-28', TRUE, 'NV04'),
('PDC86', 'CB33', 'Đặng Thị GG', '222222222', 'Nữ', '0912340031', 'HV02', 1400000, '2025-06-28', FALSE, 'NV01'),
('PDC87', 'CB34', 'Bùi Văn HH', '232323232', 'Nam', '0912340032', 'HV03', 2100000, '2025-06-28', TRUE, 'NV03'),
('PDC88', 'CB35', 'Lý Thị II', '242424242', 'Nữ', '0912340033', 'HV01', 1200000, '2025-06-28', FALSE, 'NV05'),
('PDC89', 'CB35', 'Nguyễn Văn KK', '252525252', 'Nam', '0912340034', 'HV01', 1200000, '2025-06-28', TRUE, 'NV02'),

-------- 20 chuyến bay từ 1/6 - 19/6/2025
('PDC90', 'CB36', 'Lê Văn B', '111111112', 'Nam', '0912340002', 'HV02', 1500000, '2025-05-30', TRUE, 'NV01'),
('PDC91', 'CB36', 'Trần Thị C', '111111113', 'Nữ', '0912340003', 'HV02', 1500000, '2025-05-30', TRUE, 'NV05'),
('PDC92', 'CB36', 'Nguyễn Văn D', '111111114', 'Nam', '0912340004', 'HV04', 2400000, '2025-05-30', TRUE, 'NV03'),
('PDC93', 'CB36', 'Phạm Thị E', '111111115', 'Nữ', '0912340005', 'HV04', 2400000, '2025-05-30', TRUE, 'NV02'),
('PDC94', 'CB37', 'Hoàng Văn F', '111111116', 'Nam', '0912340006', 'HV01', 1000000, '2025-05-31', TRUE, 'NV04'),
('PDC95', 'CB37', 'Đặng Thị G', '111111117', 'Nữ', '0912340007', 'HV01', 1000000, '2025-05-31', TRUE, 'NV01'),
('PDC96', 'CB37', 'Vũ Văn H', '111111118', 'Nam', '0912340008', 'HV01', 1000000, '2025-05-31', TRUE, 'NV03'),
('PDC97', 'CB38', 'Bùi Thị I', '111111119', 'Nữ', '0912340009', 'HV02', 1350000, '2025-06-01', TRUE, 'NV02'),
('PDC98', 'CB38', 'Lý Văn K', '111111120', 'Nam', '0912340010', 'HV02', 1350000, '2025-06-01', TRUE, 'NV05'),
('PDC99', 'CB38', 'Mai Thị L', '111111121', 'Nữ', '0912340011', 'HV03', 1850000, '2025-06-01', TRUE, 'NV04'),
('PDC100', 'CB38', 'Trần Văn M', '111111122', 'Nam', '0912340012', 'HV03', 1850000, '2025-06-01', TRUE, 'NV01'),
('PDC101', 'CB39', 'Đỗ Thị N', '111111123', 'Nữ', '0912340013', 'HV02', 1300000, '2025-06-02', TRUE, 'NV03'),
('PDC102', 'CB39', 'Phan Văn O', '111111124', 'Nam', '0912340014', 'HV02', 1300000, '2025-06-02', TRUE, 'NV02'),
('PDC103', 'CB39', 'Dương Thị P', '111111125', 'Nữ', '0912340015', 'HV02', 1300000, '2025-06-02', TRUE, 'NV05'),
('PDC104', 'CB40', 'Võ Văn Q', '111111126', 'Nam', '0912340016', 'HV01', 1350000, '2025-06-03', TRUE, 'NV04'),
('PDC105', 'CB40', 'Lê Thị R', '111111127', 'Nữ', '0912340017', 'HV01', 1350000, '2025-06-03', TRUE, 'NV01'),
('PDC106', 'CB40', 'Nguyễn Văn S', '111111128', 'Nam', '0912340018', 'HV03', 1850000, '2025-06-03', TRUE, 'NV03'),
('PDC107', 'CB41', 'Trần Thị T', '111111129', 'Nữ', '0912340019', 'HV01', 1000000, '2025-06-04', TRUE, 'NV02'),
('PDC108', 'CB41', 'Phạm Văn U', '111111130', 'Nam', '0912340020', 'HV01', 1000000, '2025-06-04', TRUE, 'NV05'),
('PDC109', 'CB41', 'Hoàng Thị V', '111111131', 'Nữ', '0912340021', 'HV02', 1500000, '2025-06-04', TRUE, 'NV04'),
('PDC110', 'CB42', 'Đặng Văn X', '111111132', 'Nam', '0912340022', 'HV02', 1300000, '2025-06-05', TRUE, 'NV01'),
('PDC111', 'CB42', 'Vũ Thị Y', '111111133', 'Nữ', '0912340023', 'HV02', 1300000, '2025-06-05', TRUE, 'NV03'),
('PDC112', 'CB42', 'Bùi Văn Z', '111111134', 'Nam', '0912340024', 'HV02', 1300000, '2025-06-05', TRUE, 'NV02'),
('PDC113', 'CB43', 'Lý Thị A1', '111111135', 'Nữ', '0912340025', 'HV01', 1100000, '2025-06-06', TRUE, 'NV05'),
('PDC114', 'CB44', 'Mai Văn B1', '111111136', 'Nam', '0912340026', 'HV01', 1200000, '2025-06-07', TRUE, 'NV04'),
('PDC115', 'CB44', 'Trần Thị C1', '111111137', 'Nữ', '0912340027', 'HV01', 1200000, '2025-06-07', TRUE, 'NV01'),
('PDC116', 'CB44', 'Đỗ Văn D1', '111111138', 'Nam', '0912340028', 'HV02', 1700000, '2025-06-07', TRUE, 'NV03'),
('PDC117', 'CB44', 'Phan Thị E1', '111111139', 'Nữ', '0912340029', 'HV02', 1700000, '2025-06-07', TRUE, 'NV02'),
('PDC118', 'CB45', 'Dương Văn F1', '111111140', 'Nam', '0912340030', 'HV03', 1900000, '2025-06-08', TRUE, 'NV05'),
('PDC119', 'CB45', 'Võ Thị G1', '111111141', 'Nữ', '0912340031', 'HV03', 1900000, '2025-06-08', TRUE, 'NV04'),
('PDC120', 'CB46', 'Lê Văn H1', '111111142', 'Nam', '0912340032', 'HV01', 1150000, '2025-06-09', TRUE, 'NV01'),
('PDC121', 'CB46', 'Nguyễn Thị I1', '111111143', 'Nữ', '0912340033', 'HV01', 1150000, '2025-06-09', TRUE, 'NV03'),
('PDC122', 'CB46', 'Trần Văn K1', '111111144', 'Nam', '0912340034', 'HV04', 2500000, '2025-06-09', TRUE, 'NV02'),
('PDC123', 'CB47', 'Phạm Thị L1', '111111145', 'Nữ', '0912340035', 'HV02', 1350000, '2025-06-10', TRUE, 'NV05'),
('PDC124', 'CB47', 'Hoàng Văn M1', '111111146', 'Nam', '0912340036', 'HV02', 1350000, '2025-06-10', TRUE, 'NV04'),
('PDC125', 'CB48', 'Đặng Thị N1', '111111147', 'Nữ', '0912340037', 'HV02', 1400000, '2025-06-11', TRUE, 'NV01'),
('PDC126', 'CB48', 'Vũ Văn O1', '111111148', 'Nam', '0912340038', 'HV02', 1400000, '2025-06-11', TRUE, 'NV03'),
('PDC127', 'CB48', 'Bùi Thị P1', '111111149', 'Nữ', '0912340039', 'HV03', 1950000, '2025-06-11', TRUE, 'NV02'),
('PDC128', 'CB48', 'Lý Văn Q1', '111111150', 'Nam', '0912340040', 'HV03', 1950000, '2025-06-11', TRUE, 'NV05'),
('PDC129', 'CB49', 'Mai Thị R1', '111111151', 'Nữ', '0912340041', 'HV01', 1000000, '2025-06-12', TRUE, 'NV04'),
('PDC130', 'CB49', 'Trần Văn S1', '111111152', 'Nam', '0912340042', 'HV01', 1000000, '2025-06-12', TRUE, 'NV01'),
('PDC131', 'CB49', 'Đỗ Thị T1', '111111153', 'Nữ', '0912340043', 'HV01', 1000000, '2025-06-12', TRUE, 'NV03'),
('PDC132', 'CB49', 'Phan Văn U1', '111111154', 'Nam', '0912340044', 'HV02', 1450000, '2025-06-12', TRUE, 'NV02'),
('PDC133', 'CB50', 'Dương Thị V1', '111111155', 'Nữ', '0912340045', 'HV01', 1050000, '2025-06-13', TRUE, 'NV05'),
('PDC134', 'CB50', 'Võ Văn X1', '111111156', 'Nam', '0912340046', 'HV01', 1050000, '2025-06-13', TRUE, 'NV04'),
('PDC135', 'CB50', 'Lê Thị Y1', '111111157', 'Nữ', '0912340047', 'HV01', 1050000, '2025-06-13', TRUE, 'NV01'),
('PDC136', 'CB50', 'Nguyễn Văn Z1', '111111158', 'Nam', '0912340048', 'HV03', 1750000, '2025-06-13', TRUE, 'NV03'),
('PDC137', 'CB50', 'Trần Thị A2', '111111159', 'Nữ', '0912340049', 'HV03', 1750000, '2025-06-13', TRUE, 'NV02'),
('PDC138', 'CB51', 'Phạm Văn B2', '111111160', 'Nam', '0912340050', 'HV01', 950000, '2025-06-14', TRUE, 'NV05'),
('PDC139', 'CB51', 'Hoàng Thị C2', '111111161', 'Nữ', '0912340051', 'HV01', 950000, '2025-06-14', TRUE, 'NV04'),
('PDC140', 'CB51', 'Đặng Văn D2', '111111162', 'Nam', '0912340052', 'HV01', 950000, '2025-06-14', TRUE, 'NV01'),
('PDC141', 'CB52', 'Vũ Thị E2', '111111163', 'Nữ', '0912340053', 'HV01', 1100000, '2025-06-15', TRUE, 'NV03'),
('PDC142', 'CB52', 'Bùi Văn F2', '111111164', 'Nam', '0912340054', 'HV01', 1100000, '2025-06-15', TRUE, 'NV02'),
('PDC143', 'CB52', 'Lý Thị G2', '111111165', 'Nữ', '0912340055', 'HV01', 1100000, '2025-06-15', TRUE, 'NV05'),
('PDC144', 'CB52', 'Mai Văn H2', '111111166', 'Nam', '0912340056', 'HV02', 1600000, '2025-06-15', TRUE, 'NV04'),
('PDC145', 'CB52', 'Trần Thị I2', '111111167', 'Nữ', '0912340057', 'HV02', 1600000, '2025-06-15', TRUE, 'NV01'),
('PDC146', 'CB53', 'Đỗ Văn K2', '111111168', 'Nam', '0912340058', 'HV02', 1400000, '2025-06-16', TRUE, 'NV03'),
('PDC147', 'CB53', 'Phan Thị L2', '111111169', 'Nữ', '0912340059', 'HV03', 2000000, '2025-06-16', TRUE, 'NV02'),
('PDC148', 'CB54', 'Dương Văn M2', '111111170', 'Nam', '0912340060', 'HV03', 2100000, '2025-06-17', TRUE, 'NV05'),
('PDC149', 'CB55', 'Võ Thị N2', '111111171', 'Nữ', '0912340061', 'HV01', 1200000, '2025-06-17', TRUE, 'NV04'),
('PDC150', 'CB55', 'Lê Văn O2', '111111172', 'Nam', '0912340062', 'HV01', 1200000, '2025-06-17', TRUE, 'NV02'),

---------- Tháng 1 – 5/2025 (25 chuyến)
('PDC151', 'CB56', 'Nguyễn Thị Hương', '034293817', 'Nữ', '0912345678', 'HV02', 1500000, '2025-01-08', TRUE, 'NV01'),
('PDC152', 'CB56', 'Trần Văn Long', '035628193', 'Nam', '0912345679', 'HV02', 1500000, '2025-01-08', TRUE, 'NV03'),
('PDC153', 'CB56', 'Phạm Minh Đức', '036710294', 'Nam', '0912345680', 'HV04', 2400000, '2025-01-08', TRUE, 'NV05'),
('PDC154', 'CB57', 'Lê Thị Mai', '037829305', 'Nữ', '0912345681', 'HV01', 1000000, '2025-01-13', TRUE, 'NV02'),
('PDC155', 'CB57', 'Đỗ Văn Cường', '038930416', 'Nam', '0912345682', 'HV01', 1000000, '2025-01-13', TRUE, 'NV04'),
('PDC156', 'CB57', 'Hoàng Thị Thoa', '039041527', 'Nữ', '0912345683', 'HV01', 1000000, '2025-01-13', TRUE, 'NV01'),
('PDC157', 'CB58', 'Vũ Anh Tuấn', '040152638', 'Nam', '0912345684', 'HV02', 1350000, '2025-01-18', TRUE, 'NV03'),
('PDC158', 'CB58', 'Nguyễn Thị Bích', '041263749', 'Nữ', '0912345685', 'HV02', 1350000, '2025-01-18', TRUE, 'NV05'),
('PDC159', 'CB58', 'Trần Đình Trung', '042374850', 'Nam', '0912345686', 'HV02', 1350000, '2025-01-18', TRUE, 'NV02'),
('PDC160', 'CB59', 'Phạm Thị Lan', '043485961', 'Nữ', '0912345687', 'HV02', 1300000, '2025-01-23', TRUE, 'NV04'),
('PDC161', 'CB60', 'Lê Văn Khải', '044596072', 'Nam', '0912345688', 'HV03', 1850000, '2025-01-28', TRUE, 'NV01'),
('PDC162', 'CB60', 'Đỗ Thị Minh', '045607183', 'Nữ', '0912345689', 'HV03', 1850000, '2025-01-28', TRUE, 'NV03'),
('PDC163', 'CB61', 'Hoàng Anh Khoa', '046718294', 'Nam', '0912345690', 'HV01', 1000000, '2025-02-08', TRUE, 'NV05'),
('PDC164', 'CB61', 'Vũ Thị Hồng', '047829305', 'Nữ', '0912345691', 'HV01', 1000000, '2025-02-08', TRUE, 'NV02'),
('PDC165', 'CB62', 'Nguyễn Văn Nam', '048930416', 'Nam', '0912345692', 'HV03', 1800000, '2025-02-13', TRUE, 'NV04'),
('PDC166', 'CB63', 'Trần Thị Hằng', '049041527', 'Nữ', '0912345693', 'HV01', 1100000, '2025-02-18', TRUE, 'NV01'),
('PDC167', 'CB63', 'Phạm Văn Hùng', '050152638', 'Nam', '0912345694', 'HV01', 1100000, '2025-02-18', TRUE, 'NV03'),
('PDC168', 'CB64', 'Lê Minh Thảo', '051263749', 'Nữ', '0912345695', 'HV02', 1700000, '2025-02-23', TRUE, 'NV05'),
('PDC169', 'CB64', 'Đỗ Anh Dũng', '052374850', 'Nam', '0912345696', 'HV02', 1700000, '2025-02-23', TRUE, 'NV02'),
('PDC170', 'CB65', 'Hoàng Thị Trâm', '053485961', 'Nữ', '0912345697', 'HV03', 1900000, '2025-02-26', TRUE, 'NV04'),
('PDC171', 'CB66', 'Vũ Minh Quân', '054596072', 'Nam', '0912345698', 'HV01', 1150000, '2025-03-03', TRUE, 'NV01'),
('PDC172', 'CB66', 'Nguyễn Thu Phương', '055607183', 'Nữ', '0912345699', 'HV01', 1150000, '2025-03-03', TRUE, 'NV03'),
('PDC173', 'CB66', 'Trần Văn Tùng', '056718294', 'Nam', '0912345700', 'HV04', 2500000, '2025-03-03', TRUE, 'NV05'),
('PDC174', 'CB66', 'Phạm Thị Thúy', '057829305', 'Nữ', '0912345701', 'HV04', 2500000, '2025-03-03', TRUE, 'NV02'),
('PDC175', 'CB67', 'Lê Văn Quyết', '058930416', 'Nam', '0912345702', 'HV02', 1350000, '2025-03-08', TRUE, 'NV04'),
('PDC176', 'CB67', 'Đỗ Thị Loan', '059041527', 'Nữ', '0912345703', 'HV02', 1350000, '2025-03-08', TRUE, 'NV01'),
('PDC177', 'CB67', 'Hoàng Gia Bảo', '060152638', 'Nam', '0912345704', 'HV02', 1350000, '2025-03-08', TRUE, 'NV03'),
('PDC178', 'CB68', 'Vũ Thị Kim', '061263749', 'Nữ', '0912345705', 'HV02', 1400000, '2025-03-13', TRUE, 'NV05'),
('PDC179', 'CB68', 'Nguyễn Thanh Tùng', '062374850', 'Nam', '0912345706', 'HV02', 1400000, '2025-03-13', TRUE, 'NV02'),
('PDC180', 'CB68', 'Trần Thị Diệu', '063485961', 'Nữ', '0912345707', 'HV03', 1950000, '2025-03-13', TRUE, 'NV04'),
('PDC181', 'CB68', 'Phạm Văn Thành', '064596072', 'Nam', '0912345708', 'HV03', 1950000, '2025-03-13', TRUE, 'NV01'),
('PDC182', 'CB69', 'Lê Thị Ngọc', '065607183', 'Nữ', '0912345709', 'HV01', 1000000, '2025-03-18', TRUE, 'NV03'),
('PDC183', 'CB69', 'Đỗ Minh Khang', '066718294', 'Nam', '0912345710', 'HV01', 1000000, '2025-03-18', TRUE, 'NV05'),
('PDC184', 'CB69', 'Hoàng Văn Vinh', '067829305', 'Nam', '0912345711', 'HV02', 1450000, '2025-03-18', TRUE, 'NV02'),
('PDC185', 'CB69', 'Vũ Thị Hường', '068930416', 'Nữ', '0912345712', 'HV02', 1450000, '2025-03-18', TRUE, 'NV04'),
('PDC186', 'CB70', 'Nguyễn Đức Anh', '069041527', 'Nam', '0912345713', 'HV03', 1750000, '2025-03-23', TRUE, 'NV01'),
('PDC187', 'CB70', 'Trần Thị Trang', '070152638', 'Nữ', '0912345714', 'HV03', 1750000, '2025-03-23', TRUE, 'NV03'),
('PDC188', 'CB70', 'Phạm Văn Lâm', '071263749', 'Nam', '0912345715', 'HV01', 1050000, '2025-03-23', TRUE, 'NV05'),
('PDC189', 'CB71', 'Lê Thị Thu', '072374850', 'Nữ', '0912345716', 'HV01', 950000, '2025-04-03', TRUE, 'NV02'),
('PDC190', 'CB71', 'Đỗ Văn Sơn', '073485961', 'Nam', '0912345717', 'HV01', 950000, '2025-04-03', TRUE, 'NV04'),
('PDC191', 'CB72', 'Hoàng Thị Vân', '074596072', 'Nữ', '0912345718', 'HV02', 1600000, '2025-04-08', TRUE, 'NV01'),
('PDC192', 'CB72', 'Vũ Minh Trí', '075607183', 'Nam', '0912345719', 'HV02', 1600000, '2025-04-08', TRUE, 'NV03'),
('PDC193', 'CB73', 'Nguyễn Thị Oanh', '076718294', 'Nữ', '0912345720', 'HV02', 1400000, '2025-04-13', TRUE, 'NV05'),
('PDC194', 'CB75', 'Lê Thị Yến', '077829305', 'Nữ', '0912345721', 'HV01', 1200000, '2025-04-23', TRUE, 'NV02'),
('PDC195', 'CB75', 'Đỗ Văn Phúc', '078930416', 'Nam', '0912345722', 'HV01', 1200000, '2025-04-23', TRUE, 'NV04'),
('PDC196', 'CB76', 'Hoàng Thị Dung', '079041527', 'Nữ', '0912345723', 'HV02', 1500000, '2025-04-29', TRUE, 'NV01'),
('PDC197', 'CB78', 'Vũ Văn Long', '080152638', 'Nam', '0912345724', 'HV03', 1850000, '2025-05-08', TRUE, 'NV03'),
('PDC198', 'CB78', 'Nguyễn Thị Loan', '081263749', 'Nữ', '0912345725', 'HV03', 1850000, '2025-05-08', TRUE, 'NV05'),
('PDC199', 'CB78', 'Trần Đình Quân', '082374850', 'Nam', '0912345726', 'HV02', 1350000, '2025-05-08', TRUE, 'NV02'),
('PDC200', 'CB78', 'Phạm Thị Hương', '083485961', 'Nữ', '0912345727', 'HV02', 1350000, '2025-05-08', TRUE, 'NV04'),
('PDC201', 'CB79', 'Lê Văn Hiếu', '084596072', 'Nam', '0912345728', 'HV02', 1300000, '2025-05-13', TRUE, 'NV01'),
('PDC202', 'CB79', 'Đỗ Thị Thanh', '085607183', 'Nữ', '0912345729', 'HV02', 1300000, '2025-05-13', TRUE, 'NV03'),
('PDC203', 'CB80', 'Hoàng Văn Khang', '086718294', 'Nam', '0912345730', 'HV03', 1850000, '2025-05-18', TRUE, 'NV05'),
('PDC204', 'CB80', 'Vũ Thị Mai', '087829305', 'Nữ', '0912345731', 'HV03', 1850000, '2025-05-18', TRUE, 'NV02'),
('PDC205', 'CB80', 'Nguyễn Văn Mạnh', '088930416', 'Nam', '0912345732', 'HV01', 1350000, '2025-05-18', TRUE, 'NV04'),
('PDC206', 'CB80', 'Trần Thị Thu', '089041527', 'Nữ', '0912345733', 'HV01', 1350000, '2025-05-18', TRUE, 'NV01'),

----- 20 chuyến bay năm 2024 
('PDC207', 'CB81', 'Trần Văn A', '111222333', 'Nam', '0912345678', 'HV01', 1000000, '2024-01-08', TRUE, 'NV01'),
('PDC208', 'CB81', 'Nguyễn Thị B', '111222334', 'Nữ', '0912345679', 'HV01', 1000000, '2024-01-08', TRUE, 'NV02'),
('PDC209', 'CB81', 'Phạm Văn C', '111222335', 'Nam', '0912345680', 'HV02', 1500000, '2024-01-08', TRUE, 'NV03'),
('PDC210', 'CB82', 'Lê Thị D', '111222336', 'Nữ', '0912345681', 'HV02', 1300000, '2024-02-13', TRUE, 'NV04'),
('PDC211', 'CB82', 'Hoàng Văn E', '111222337', 'Nam', '0912345682', 'HV02', 1300000, '2024-02-13', TRUE, 'NV05'),
('PDC212', 'CB83', 'Đỗ Thị F', '111222338', 'Nữ', '0912345683', 'HV01', 1100000, '2024-03-18', TRUE, 'NV01'),
('PDC213', 'CB84', 'Vũ Văn G', '111222339', 'Nam', '0912345684', 'HV01', 1200000, '2024-04-23', TRUE, 'NV02'),
('PDC214', 'CB84', 'Bùi Thị H', '111222340', 'Nữ', '0912345685', 'HV01', 1200000, '2024-04-23', TRUE, 'NV03'),
('PDC215', 'CB84', 'Trần Văn I', '111222341', 'Nam', '0912345686', 'HV01', 1200000, '2024-04-23', TRUE, 'NV04'),
('PDC216', 'CB84', 'Nguyễn Thị J', '111222342', 'Nữ', '0912345687', 'HV02', 1700000, '2024-04-23', TRUE, 'NV05'),
('PDC217', 'CB84', 'Phạm Văn K', '111222343', 'Nam', '0912345688', 'HV02', 1700000, '2024-04-23', TRUE, 'NV01'),
('PDC218', 'CB85', 'Lê Thị L', '111222344', 'Nữ', '0912345689', 'HV03', 1900000, '2024-05-28', TRUE, 'NV02'),
('PDC219', 'CB85', 'Hoàng Văn M', '111222345', 'Nam', '0912345690', 'HV03', 1900000, '2024-05-28', TRUE, 'NV03'),
('PDC220', 'CB86', 'Đỗ Thị N', '111222346', 'Nữ', '0912345691', 'HV04', 2500000, '2024-06-03', TRUE, 'NV04'),
('PDC221', 'CB86', 'Vũ Văn O', '111222347', 'Nam', '0912345692', 'HV04', 2500000, '2024-06-03', TRUE, 'NV05'),
('PDC222', 'CB87', 'Bùi Thị P', '111222348', 'Nữ', '0912345693', 'HV02', 1350000, '2024-07-08', TRUE, 'NV01'),
('PDC223', 'CB88', 'Trần Văn Q', '111222349', 'Nam', '0912345694', 'HV03', 1950000, '2024-08-13', TRUE, 'NV02'),
('PDC224', 'CB88', 'Nguyễn Thị R', '111222350', 'Nữ', '0912345695', 'HV03', 1950000, '2024-08-13', TRUE, 'NV03'),
('PDC225', 'CB89', 'Phạm Văn S', '111222351', 'Nam', '0912345696', 'HV02', 1450000, '2024-09-18', TRUE, 'NV04'),
('PDC226', 'CB89', 'Lê Thị T', '111222352', 'Nữ', '0912345697', 'HV02', 1450000, '2024-09-18', TRUE, 'NV05'),
('PDC227', 'CB89', 'Hoàng Văn U', '111222353', 'Nam', '0912345698', 'HV02', 1450000, '2024-09-18', TRUE, 'NV01'),
('PDC228', 'CB90', 'Đỗ Thị V', '111222354', 'Nữ', '0912345699', 'HV01', 1050000, '2024-10-23', TRUE, 'NV02'),
('PDC229', 'CB90', 'Vũ Văn W', '111222355', 'Nam', '0912345700', 'HV01', 1050000, '2024-10-23', TRUE, 'NV03'),
('PDC230', 'CB91', 'Bùi Thị X', '111222356', 'Nữ', '0912345701', 'HV01', 950000, '2024-11-08', TRUE, 'NV04'),
('PDC231', 'CB91', 'Trần Văn Y', '111222357', 'Nam', '0912345702', 'HV01', 950000, '2024-11-08', TRUE, 'NV05'),
('PDC232', 'CB92', 'Nguyễn Thị Z', '111222358', 'Nữ', '0912345703', 'HV01', 1100000, '2024-12-13', TRUE, 'NV01'),
('PDC233', 'CB93', 'Phạm Văn AA', '111222359', 'Nam', '0912345704', 'HV03', 2000000, '2024-01-18', TRUE, 'NV02'),
('PDC234', 'CB93', 'Lê Thị BB', '111222360', 'Nữ', '0912345705', 'HV03', 2000000, '2024-01-18', TRUE, 'NV03'),
('PDC235', 'CB94', 'Hoàng Văn CC', '111222361', 'Nam', '0912345706', 'HV03', 2100000, '2024-02-23', TRUE, 'NV04'),
('PDC236', 'CB94', 'Đỗ Thị DD', '111222362', 'Nữ', '0912345707', 'HV03', 2100000, '2024-02-23', TRUE, 'NV05'),
('PDC237', 'CB94', 'Vũ Văn EE', '111222363', 'Nam', '0912345708', 'HV03', 2100000, '2024-02-23', TRUE, 'NV01'),
('PDC238', 'CB95', 'Bùi Thị FF', '111222364', 'Nữ', '0912345709', 'HV01', 1200000, '2024-03-28', TRUE, 'NV02'),
('PDC239', 'CB95', 'Trần Văn GG', '111222365', 'Nam', '0912345710', 'HV01', 1200000, '2024-03-28', TRUE, 'NV03'),
('PDC240', 'CB96', 'Nguyễn Thị HH', '111222366', 'Nữ', '0912345711', 'HV04', 2400000, '2024-04-03', TRUE, 'NV04'),
('PDC241', 'CB96', 'Phạm Văn II', '111222367', 'Nam', '0912345712', 'HV04', 2400000, '2024-04-03', TRUE, 'NV05'),
('PDC242', 'CB97', 'Lê Thị JJ', '111222368', 'Nữ', '0912345713', 'HV01', 1000000, '2024-05-08', TRUE, 'NV01'),
('PDC243', 'CB97', 'Hoàng Văn KK', '111222369', 'Nam', '0912345714', 'HV01', 1000000, '2024-05-08', TRUE, 'NV02'),
('PDC244', 'CB98', 'Đỗ Thị LL', '111222370', 'Nữ', '0912345715', 'HV02', 1350000, '2024-06-13', TRUE, 'NV03'),
('PDC245', 'CB98', 'Vũ Văn MM', '111222371', 'Nam', '0912345716', 'HV02', 1350000, '2024-06-13', TRUE, 'NV04'),
('PDC246', 'CB98', 'Bùi Thị NN', '111222372', 'Nữ', '0912345717', 'HV02', 1350000, '2024-06-13', TRUE, 'NV05'),
('PDC247', 'CB99', 'Trần Văn OO', '111222373', 'Nam', '0912345718', 'HV02', 1300000, '2024-07-18', TRUE, 'NV01'),
('PDC248', 'CB99', 'Nguyễn Thị PP', '111222374', 'Nữ', '0912345719', 'HV02', 1300000, '2024-07-18', TRUE, 'NV02'),
('PDC249', 'CB100', 'Phạm Văn QQ', '111222375', 'Nam', '0912345720', 'HV01', 1350000, '2024-08-23', TRUE, 'NV03'),

----- 20 chuyến bay năm 2023
('PDC250', 'CB101', 'Nguyễn Thị Hương', '012345678912', 'Nữ', '0901234567', 'HV01', 1000000, '2023-01-03', TRUE, 'NV01'),
('PDC251', 'CB101', 'Trần Văn Tùng', '012345678913', 'Nam', '0901234568', 'HV01', 1000000, '2023-01-03', TRUE, 'NV02'),
('PDC252', 'CB101', 'Lê Thu Thủy', '012345678914', 'Nữ', '0901234569', 'HV02', 1500000, '2023-01-03', TRUE, 'NV03'),
('PDC253', 'CB101', 'Phạm Minh Đức', '012345678915', 'Nam', '0901234570', 'HV02', 1500000, '2023-01-03', TRUE, 'NV04'),
('PDC254', 'CB101', 'Hoàng Ngọc Ánh', '012345678916', 'Nữ', '0901234571', 'HV02', 1500000, '2023-01-03', TRUE, 'NV05'),
('PDC255', 'CB102', 'Vũ Anh Khoa', '012345678917', 'Nam', '0901234572', 'HV02', 1300000, '2023-02-08', TRUE, 'NV01'),
('PDC256', 'CB103', 'Đặng Thúy Nga', '012345678918', 'Nữ', '0901234573', 'HV01', 1100000, '2023-03-13', TRUE, 'NV02'),
('PDC257', 'CB103', 'Bùi Trung Kiên', '012345678919', 'Nam', '0901234574', 'HV01', 1100000, '2023-03-13', TRUE, 'NV03'),
('PDC258', 'CB103', 'Ngô Lan Anh', '012345678920', 'Nữ', '0901234575', 'HV01', 1100000, '2023-03-13', TRUE, 'NV04'),
('PDC259', 'CB104', 'Dương Quốc Việt', '012345678921', 'Nam', '0901234576', 'HV01', 1200000, '2023-04-18', TRUE, 'NV05'),
('PDC260', 'CB104', 'Lê Thanh Bình', '012345678922', 'Nam', '0901234577', 'HV01', 1200000, '2023-04-18', TRUE, 'NV01'),
('PDC261', 'CB104', 'Trần Thị Mai', '012345678923', 'Nữ', '0901234578', 'HV02', 1700000, '2023-04-18', TRUE, 'NV02'),
('PDC262', 'CB104', 'Hoàng Gia Huy', '012345678924', 'Nam', '0901234579', 'HV02', 1700000, '2023-04-18', TRUE, 'NV03'),
('PDC263', 'CB106', 'Phạm Thị Lan', '012345678925', 'Nữ', '0901234580', 'HV01', 1150000, '2023-06-28', TRUE, 'NV04'),
('PDC264', 'CB106', 'Nguyễn Đức Thắng', '012345678926', 'Nam', '0901234581', 'HV01', 1150000, '2023-06-28', TRUE, 'NV05'),
('PDC265', 'CB107', 'Đỗ Hải Yến', '012345678927', 'Nữ', '0901234582', 'HV02', 1350000, '2023-07-03', TRUE, 'NV01'),
('PDC266', 'CB108', 'Nguyễn Thị Hoa', '012345678928', 'Nữ', '0901234583', 'HV02', 1400000, '2023-08-08', TRUE, 'NV02'),
('PDC267', 'CB108', 'Trần Đình Nam', '012345678929', 'Nam', '0901234584', 'HV02', 1400000, '2023-08-08', TRUE, 'NV03'),
('PDC268', 'CB108', 'Lý Kim Chi', '012345678930', 'Nữ', '0901234585', 'HV03', 1950000, '2023-08-08', TRUE, 'NV04'),
('PDC269', 'CB108', 'Võ Thành Công', '012345678931', 'Nam', '0901234586', 'HV03', 1950000, '2023-08-08', TRUE, 'NV05'),
('PDC270', 'CB108', 'Bùi Bích Ngọc', '012345678932', 'Nữ', '0901234587', 'HV03', 1950000, '2023-08-08', TRUE, 'NV01'),
('PDC271', 'CB109', 'Nguyễn Hồng Minh', '012345678933', 'Nữ', '0901234588', 'HV02', 1450000, '2023-09-13', TRUE, 'NV02'),
('PDC272', 'CB109', 'Lê Văn Hiếu', '012345678934', 'Nam', '0901234589', 'HV02', 1450000, '2023-09-13', TRUE, 'NV03'),
('PDC273', 'CB110', 'Trần Minh Anh', '012345678935', 'Nữ', '0901234590', 'HV03', 1750000, '2023-10-18', TRUE, 'NV04'),
('PDC274', 'CB110', 'Phạm Quốc An', '012345678936', 'Nam', '0901234591', 'HV03', 1750000, '2023-10-18', TRUE, 'NV05'),
('PDC275', 'CB111', 'Đỗ Thị Quyên', '012345678937', 'Nữ', '0901234592', 'HV01', 950000, '2023-11-23', TRUE, 'NV01'),
('PDC276', 'CB111', 'Hoàng Văn Lộc', '012345678938', 'Nam', '0901234593', 'HV01', 950000, '2023-11-23', TRUE, 'NV02'),
('PDC277', 'CB111', 'Nguyễn Thị Bích', '012345678939', 'Nữ', '0901234594', 'HV01', 950000, '2023-11-23', TRUE, 'NV03'),
('PDC278', 'CB112', 'Lê Hữu Nghĩa', '012345678940', 'Nam', '0901234595', 'HV01', 1100000, '2023-12-28', TRUE, 'NV04'),
('PDC279', 'CB112', 'Vũ Thị Thanh', '012345678941', 'Nữ', '0901234596', 'HV01', 1100000, '2023-12-28', TRUE, 'NV05'),
('PDC280', 'CB112', 'Trần Quang Vinh', '012345678942', 'Nam', '0901234597', 'HV02', 1600000, '2023-12-28', TRUE, 'NV01'),
('PDC281', 'CB112', 'Phạm Gia Linh', '012345678943', 'Nữ', '0901234598', 'HV02', 1600000, '2023-12-28', TRUE, 'NV02'),
('PDC282', 'CB112', 'Đào Duy Anh', '012345678944', 'Nam', '0901234599', 'HV02', 1600000, '2023-12-28', TRUE, 'NV03'),
('PDC283', 'CB113', 'Nguyễn Thành Đạt', '012345678945', 'Nam', '0901234600', 'HV02', 1400000, '2023-02-27', TRUE, 'NV04'),
('PDC284', 'CB113', 'Lê Thị Mai', '012345678946', 'Nữ', '0901234601', 'HV02', 1400000, '2023-02-27', TRUE, 'NV05'),
('PDC285', 'CB113', 'Hoàng Văn Cường', '012345678947', 'Nam', '0901234602', 'HV02', 1400000, '2023-02-27', TRUE, 'NV01'),
('PDC286', 'CB113', 'Trần Hữu Phúc', '012345678948', 'Nam', '0901234603', 'HV03', 2000000, '2023-02-27', TRUE, 'NV02'),
('PDC287', 'CB114', 'Phạm Thị Thảo', '012345678949', 'Nữ', '0901234604', 'HV03', 2100000, '2023-04-29', TRUE, 'NV03'),
('PDC288', 'CB114', 'Nguyễn Minh Quân', '012345678950', 'Nam', '0901234605', 'HV03', 2100000, '2023-04-29', TRUE, 'NV04'),
('PDC289', 'CB116', 'Lê Thị Yến', '012345678951', 'Nữ', '0901234606', 'HV02', 1500000, '2023-08-30', TRUE, 'NV05'),
('PDC290', 'CB116', 'Hoàng Bá Long', '012345678952', 'Nam', '0901234607', 'HV02', 1500000, '2023-08-30', TRUE, 'NV01'),
('PDC291', 'CB116', 'Trần Ngọc Bích', '012345678953', 'Nữ', '0901234608', 'HV02', 1500000, '2023-08-30', TRUE, 'NV02'),
('PDC292', 'CB116', 'Võ Mạnh Hùng', '012345678954', 'Nam', '0901234609', 'HV04', 2400000, '2023-08-30', TRUE, 'NV03'),
('PDC293', 'CB116', 'Đắng Kim Ngân', '012345678955', 'Nữ', '0901234610', 'HV04', 2400000, '2023-08-30', TRUE, 'NV04'),
('PDC294', 'CB117', 'Bùi Thanh Duy', '012345678956', 'Nam', '0901234611', 'HV01', 1000000, '2023-10-30', TRUE, 'NV05'),
('PDC295', 'CB117', 'Nguyễn Thị Ánh', '012345678957', 'Nữ', '0901234612', 'HV01', 1000000, '2023-10-30', TRUE, 'NV01'),
('PDC296', 'CB117', 'Trần Minh Thắng', '012345678958', 'Nam', '0901234613', 'HV01', 1000000, '2023-10-30', TRUE, 'NV02'),
('PDC297', 'CB118', 'Lê Xuân Trường', '012345678959', 'Nam', '0901234614', 'HV02', 1350000, '2023-01-13', TRUE, 'NV03'),
('PDC298', 'CB118', 'Phạm Thanh Vân', '012345678960', 'Nữ', '0901234615', 'HV02', 1350000, '2023-01-13', TRUE, 'NV04'),
('PDC299', 'CB118', 'Nguyễn Văn Tiến', '012345678961', 'Nam', '0901234616', 'HV03', 1850000, '2023-01-13', TRUE, 'NV05'),
('PDC300', 'CB120', 'Hoàng Văn Nam', '012345678962', 'Nam', '0901234617', 'HV01', 1350000, '2023-08-13', TRUE, 'NV01'),
('PDC301', 'CB120', 'Lý Thị Kiều', '012345678963', 'Nữ', '0901234618', 'HV01', 1350000, '2023-08-13', TRUE, 'NV02');