# TongueDiagnosis

## 一、项目架构

TongueDiagnosis{

​	application (后端) {
​		config (后端配置)

​		core (核心算法)

​		models (数据库模型)

​		net (神经网络模型)

​		orm (数据库映射模型)

​		routes (路由)

​		init.py (后端初始化)

​	}

​	frontend (前端) {

​		cypress (调试文件)

​		public (静态文件)

​		src (源代码) {

​			assets (资产)

​			components (自己写的组件)

​			router (路由)

​			stores (不知道...)

​			views (视图，近似于pages)

​			App.vue (Vue应用根组件)

​			main.js (Vue应用入口)

​		}

​		index.html (网站入口)

​		package.json (所有包管理配置)

​		vite.config.js (脚手架配置，打包代理跨域配置)

​	}

​	.gitignore (git忽略)

​	run.py (整体应用入口)

}

## 二、开发环境

1. 安装python依赖

​	（1）pip install sqlalchemy

​	（2）pip install fastapi

​	（3）pip install uvicorn

​	（4）pip install jose
2. 安装npm依赖

​	（1）[Node.js (nodejs.org)](https://nodejs.org/en)安装node.js，20.11.1 LTS版本

​	安装完成后，在命令行运行

​	node -v

​	若出现版本号，则安装成功

​	（2）添加npm到系统环境变量的Path下。将npm文件地bin文件目录添加到环境变量中。

​	e.g. "E:\nodejs\node_modules\npm\bin"

​	（3）在项目工作目录下，在终端运行

​	cd frontend

​	npm install 

​	npm run dev

​	若出现

​	Local: http://localhost:****/

​	则成功

3. SQL数据库配置：暂无

4. git使用：

   （1）开发中分支命名为：

   ​	姓名首字母小写_dev

   ​	e.g. yhy_dev

   ​	分支完善后，合并进入主开发分支dev_main

   ​	当前阶段开发任务完成且测试通过，合并进入mian分支

   （2）提交注意：

   ​	提交前先拉取最新代码

   ​	提交前先运行测试

   ​	提交前先进行代码格式化

   

​	
