FROM python:3.11-slim
LABEL authors="tainya3"

# 安装基本依赖
RUN apt-get update
RUN apt install libgl1-mesa-glx -y
RUN apt-get install -y --no-install-recommends
RUN apt-get install libglib2.0-dev -y


# 设置工作目录
WORKDIR /app

# 安装依赖
COPY /requirements.txt .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

RUN pip install -i https://mirrors.aliyun.com/pypi/simple python-multipart

RUN pip install opencv-python-headless -i https://mirrors.aliyun.com/pypi/simple



# 复制文件
COPY . .


# 启动服务
CMD ["python", "run.py"]