import os


def write(data, path, mode='a', encoding='utf-8'):
	try:

		with open(path, mode, encoding=encoding) as file:
			for line in data:
				file.write(line)
		return True
	except Exception as e:
		print(f"Có lỗi xảy ra: {e}")
		return False


def read(path, mode='r'):
	try:
		with open(path, mode) as file:
			du_lieu = [line.strip().split(',') for line in file.readlines()]
		return du_lieu
	except Exception as e:
		print(f"Có lỗi xảy ra khi đọc data: {e}")
		return None


def clearData(path):
	try:
		# Open the data in write mode, which clears its contents
		with open(path, "w") as file:
			pass  # This effectively clears the data

		print("File cleared successfully.")
	except Exception as e:
		print(f"Có lỗi xảy ra khi đọc data: {e}")
		return None
