import os
import statistics

from app import constant, data


# hàm hiển thị các lựa chọn, nhận lựa chọn của người dùng để điều hướng đến view người dùng chọn
def view():
	while True:
		try:
			menu()
			choice = int(input("Xin hãy nhập lựa chọn của bạn: "))
			match choice:
				case 1:
					view_cham_thi()
				case 2:
					view_thong_ke()
				case 3:
					view_cap_nhat_dap_an()
				case 4:
					print("Bạn đã thoát hệ thống")
					break
				case _:
					print("Lựa chọn của bạn nằm ngoài khả năng hệ thống, vui lòng nhập lại!")
					continue
		except ValueError:
			print("Lựa chọn phải là số nguyên, vui lòng nhập lại!")


# hiện thị menu các lựa chọn
def menu():
	print("==========Menu===========")
	print("1.Chấm điểm thi")
	print("2.Thống kê điểm số")
	print("3.Cập nhật đáp án")
	print("4.Thoát")


# hiển thị view cập nhật đáp án, nhận các đáp án cần cập nhật của người dùng
def view_cap_nhat_dap_an():
	while True:
		try:
			log("=========== Update answer  =============")
			log('DS đáp án:' + ','.join(constant.ANSWERS))
			ds_dap_an = input("Xin mời nhập ds đáp án (cách nhau bằng dấu phẩy): ")
			ds_dap_an = ds_dap_an.split(',')
			data.write(constant.FILE_ANSWER_DIR, ds_dap_an)
			constant.ANSWERS = ds_dap_an
			log("Cập nhật đáp án thành công")
			return
		except Exception as e:
			log(f"Lỗi trong quá trình cập nhật đáp án: {e}")
			log("Xin mời nhập lại")


# hiển thị view chấm điểm bài thi, tiếp nhận và điều hướng đến chức năng mà người dùng chọn
def view_cham_thi():
	while True:
		try:
			menu_cham_thi()
			choice = int(input("Xin hãy nhập lựa chọn của bạn: "))
			match choice:
				case 1:
					ds_file_thu_muc(constant.UN_GRADED_DIR)
				case 2:
					ds_file_thu_muc(constant.GRADED_DIR)
				case 3:
					log("============Chấm thi============")
					view_chon_lop()
				case 4:
					print("Bạn đã thoát hệ thống")
					break
				case _:
					print("Lựa chọn của bạn nằm ngoài khả năng hệ thống, vui lòng nhập lại!")
					continue
		except ValueError:
			print("Lựa chọn phải là số nguyên, vui lòng nhập lại!")


# Hiển thị menu chấm thi
def menu_cham_thi():
	print("==========Menu Chấm thi===========")
	print("1.Danh sách bài thi chưa chấm")
	print("2.Danh sách các bài đã chấm")
	print("3.Chọn lớp chấm bài ")
	print("4.Thoát")


# Hiển thị view chọn lớp, tiếp nhận và thực hiện việc chọn lớp để chấm điểm và thống kê
def view_chon_lop():
	while True:
		try:
			lop_cham_diem = input("Xin hãy nhập lựa chọn của bạn(vd: class1): ")
			log(f"Chọn lớp để chấm điểm: {lop_cham_diem}")
			ten_file = constant.SLASH + lop_cham_diem + constant.TXT
			lop_cham_diem_dir = constant.UN_GRADED_DIR + ten_file
			ds_kq_bai_thi = data.read(lop_cham_diem_dir)
			log(f"Mở thành công file {lop_cham_diem}")
			if cham_thi(ds_kq_bai_thi, lop_cham_diem):
				thong_ke(lop_cham_diem)

			choice = input("Bạn có muốn thoát không(1: có) :")
			if choice == '1':
				break

		except FileNotFoundError:
			print("Không tìm thấy file yêu cầu! vui lòng nhập lại!")


# Chấm điểm cái bài thi của một lớp
def cham_thi( ds_kq_bai_thi: list, lop_cham_diem: str ) -> bool:
	try:
		log("*** Phân tích ***")
		ma_hoc_sinh = None
		kq_lop_dir = constant.GRADED_DIR + constant.SLASH + lop_cham_diem + "_" + constant.GRADED + constant.TXT
		data.clear_data(kq_lop_dir)
		for bai_thi in ds_kq_bai_thi:
			ma_hoc_sinh = bai_thi[0]
			ds_kq_bai_lam = bai_thi[1:]
			if not hop_le_ma_hs(ma_hoc_sinh):
				log(bai_thi)
				continue
			if not hop_le_ket_qua(ds_kq_bai_lam):
				log(bai_thi)
				continue
			tong_diem, ds_ket_qua = tinh_tong_diem(ds_kq_bai_lam)
			ket_qua = f"{ma_hoc_sinh},{','.join(ds_ket_qua)},{tong_diem}\n"
			if not data.write(ket_qua, kq_lop_dir):
				log(f"Có lỗi xảy ra khi ghi kết quả có mã [{ma_hoc_sinh}] vào file!")
				continue
		return True
	except Exception as e:
		log(f"Có lỗi xảy ra khi chấm kết quả: {e}")
		return False


# Hiển thị view thống kê, tiếp nhận và thực hiện hành động chọn lớp để thống kê
def view_thong_ke():
	while True:
		try:
			log("============Thống kê============")
			log("*** Danh sách lớp đã được chấm ***")
			ds_file_thu_muc(constant.GRADED_DIR)
			lop_cham_diem = input("Xin hãy nhập lựa chọn của bạn(vd: class1): ")
			log(f"Chọn lớp để phân tích: {lop_cham_diem}")
			thong_ke(lop_cham_diem)
			choice = input("Bạn có muốn thoát không(1: có) :")
			if choice == '1':
				break
		except FileNotFoundError:
			print("Không tìm thấy file yêu cầu! vui lòng nhập lại!")


# thống kê điểm thi của lớp đã chấm điểm
def thong_ke( lop_cham_diem ):
	log("*** Thống kê ***")
	kq_lop_dir = constant.GRADED_DIR + constant.SLASH + lop_cham_diem + "_" + constant.GRADED + constant.TXT
	ds_kq_lop = data.read(kq_lop_dir)
	ds_tong_diem = []
	ds_dap_an = []
	for i in ds_kq_lop:
		ds_tong_diem.append(i[-1])
		ds_dap_an.append(i[1:-1])

	phan_tich_diem(ds_tong_diem)
	tinh_ty_le_sai_bo_qua(ds_dap_an, len(ds_kq_lop))


# phân thích điểm sau khi đã chấm
def phan_tich_diem( ds_tong_diem ):
	ds_kq = sorted(ds_tong_diem)
	so_luong_diem_cao = sum([1 for i in ds_kq if int(i) > 80])
	min_kq = int(ds_kq[0])
	max_kq = int(ds_kq[-1])
	mean_kq = sum([int(i) for i in ds_kq]) / len(ds_kq)
	range_kq = max_kq - min_kq
	median_kq = statistics.mean([int(i) for i in ds_kq])

	log(f"Số lượng học sinh đạt điểm cao là: {so_luong_diem_cao}")
	log(f"Điểm trung bình là: {mean_kq:.{4}}")
	log(f"Điểm cao nhất là: {max_kq}")
	log(f"Điểm thấp nhất là: {min_kq}")
	log(f"Chênh lệch điểm là: {range_kq}")
	log(f"Điểm có giá trị trung vị là: {median_kq:.{4}}")


# Tính toán tỷ lệ của các câu có đáp án sai hay bỏ qua
def tinh_ty_le_sai_bo_qua( ds_dap_an: list, so_lg_bai_lam ):
	tong_so_dap_an_bo_trong = 0
	tong_so_dap_an_sai = 0

	ds_so_lg_dap_an_sai = [[i + 1, 0] for i in range(25)]
	ds_so_lg_dap_an_bo_qua = [[i + 1, 0] for i in range(25)]
	for element in ds_dap_an:
		for i, dap_an in enumerate(element):
			if dap_an == '_':
				ds_so_lg_dap_an_bo_qua[i][1] += 1
				tong_so_dap_an_bo_trong += 1
			else:
				ds_so_lg_dap_an_sai[i][1] += 1
				tong_so_dap_an_sai += 1

	ds_so_lg_dap_an_sai = sorted(ds_so_lg_dap_an_sai, key = lambda x: x[1], reverse = True)
	ds_so_lg_dap_an_bo_qua = sorted(ds_so_lg_dap_an_bo_qua, key = lambda x: x[1], reverse = True)
	for element in ds_so_lg_dap_an_bo_qua:
		max = ds_so_lg_dap_an_bo_qua[0][1]
		if element[1] != 0 and element[1] == max:
			log(f"Số thứ tự câu hỏi [{element[0]}],"
			    f"số lượng học sinh bỏ qua [{element[1]}],"
			    f"tỉ lệ bị bỏ qua[{(element[1] / so_lg_bai_lam * 100):.{4}}]")
		else:
			break
	for element in ds_so_lg_dap_an_sai:
		max = ds_so_lg_dap_an_sai[0][1]
		if element[1] != 0 and element[1] == max:
			log(f"Số thứ tự câu hỏi [{element[0]}]"
			    f",số lượng học sinh trả lời sai [{element[1]}]"
			    f",tỉ lệ bị sai [{(element[1] / so_lg_bai_lam * 100):.{4}}%]"
			    )
		else:
			break


# Tính tổng điểm của bài thi
def tinh_tong_diem( ds_kq_bai_lam: list ):
	tong_diem = 0
	ket_qua = []
	for i in range(25):
		if ds_kq_bai_lam[i] == constant.ANSWERS[i]:
			tong_diem += 4
			ket_qua.append("T")
		elif ds_kq_bai_lam[i] == '':
			ket_qua.append("_")
			continue
		else:
			ket_qua.append("F")
			tong_diem -= 1
	return tong_diem, ket_qua


# kiểm tra kết qua có hợp lệ hay không
def hop_le_ket_qua( ds_kq: list ) -> bool:
	if len(ds_kq) != 25:
		log("Dữ liệu đáp án không hợp lệ : Không chứa đầy đủ 25 kết quả")
		return False
	for element in ds_kq:
		if element not in tuple(("A", "B", "C", "D", "")):
			log("Dữ liệu đáp án không hợp lệ : Kết quả không đúng định dạng")
			return False
	return True


# Kiểm tra mã học sinh có hợp lệ hay không
def hop_le_ma_hs( ma_hoc_sinh: list ) -> bool:
	if len(ma_hoc_sinh) != 9:
		log("Dữ liệu không hợp lệ : Mã học sinh phải có 9 ký tự")
		return False

	ky_tu_1: str = ma_hoc_sinh[0]
	if ky_tu_1.isdigit():
		log("Dữ liệu không hợp lệ : Ký tự đầu tiên phải là chữ")
		return False

	ky_tu_con_lai: str = ma_hoc_sinh[1:]
	for element in ky_tu_con_lai:
		if not element.isdigit():
			log("Dữ liệu không hợp lệ : 8 ký tự cuối mã học sinh phải là số")
			return False

	return True


# hiện thị danh sách các file dựa trên đường dẫn folder truyền vào
def ds_file_thu_muc( directory ):
	if not os.path.isdir(directory):
		print("Thư mục không tồn tại.")
		return

	# Liệt kê các tệp trong thư mục
	files = os.listdir(directory)
	if len(files) == 0:
		print("Không có dữ liệu")
	# In danh sách tệp ra console
	print("Các tệp trong thư mục", directory, "là:")
	for file in files:
		print(file.replace(constant.TXT, ''))


# thực hiện ghi dữ liệu vào report file
def log( message ):
	print(message)
	data.write(str(message) + "\n", constant.FILE_REPORT_DIR)


# hàm chính để chạy toàn bộ app, thực hiện dọc file answer đã lưu vào file
def main():
	try:
		constant.ANSWERS = data.read(constant.FILE_ANSWER_DIR)[0]
	except FileNotFoundError:
		log("Lỗi không tìm thấy file đáp án")
		return
	view()


if __name__ == "__main__":
	main()
