import random

# Danh sách ban đầu
initial_list = ['N00000045', 'D', 'C', 'B', 'B', 'A', 'D', 'A', 'D', 'B', 'A', 'B', 'B', 'C', 'C', 'B', 'A', 'D', 'B',
                'B', 'C', 'D', 'D', 'B', 'A', 'B']


def get_answers():
	try:
		with open('../data/answer/answer.txt', mode='r') as file:
			ds_lines = file.readlines()
			du_lieu = ds_lines[0].strip().split(',')
		return du_lieu
	except Exception as e:
		print(f"Có lỗi xảy ra khi đọc data: {e}")
		return None


# Hàm để tạo danh sách đáp án mới
def create_new_answer():
	return ','.join(random.choice(['D', 'C', 'B', 'A']) for _ in range(25))


# Hàm để tạo danh sách mới
def create_new_list(initial_list, min_similarity=0.5):
	initial_list = initial_list[0:1]
	initial_list = initial_list + get_answers()
	new_lists = []
	for i in range(30):
		new_list = []
		for item in initial_list:
			# Random số từ 0 đến 1
			rand = random.random()
			# Nếu số random lớn hơn min_similarity thì giữ nguyên giá trị từ danh sách ban đầu
			if rand >= min_similarity:
				new_list.append(item)
			else:
				# Ngược lại, chọn một giá trị mới từ ['D', 'C', 'B', 'A','']
				new_item = random.choice(['D', 'C', 'B', 'A', ''])
				new_list.append(new_item)

		new_lists.append(new_list)

	return new_lists


# Tạo danh sách mới
new_lists = create_new_list(initial_list, min_similarity=0.5)


#In ra đáp án mới
print(create_new_answer())

# In ra danh sách mới
for i, lst in enumerate(new_lists, start=31):
	# Tạo chuỗi số dạng 00000001 -> 00000060
	num_str = str(i).zfill(8)
	# Thay thế ký tự số trong chuỗi ban đầu
	new_list_id = 'N' + num_str
	# Thay thế ký tự đầu tiên của danh sách mới
	lst[0] = new_list_id
	# Loại bỏ các ký tự không mong muốn và giữ lại dấu phẩy
	lst_str = ','.join(filter(lambda x: x not in [' ', '[', ']', ','], lst))
	print(lst_str)
