# 数据库工具服务器 (DB Tool Server)

这是一个基于Flask的数据库工具服务器，提供数据库表管理、查询接口和日志监控功能。该项目最初基于SQLite开发，但设计上支持将来迁移到Oracle数据库。

## 功能特点

- 部门(DEPT)、员工(EMP)、奖金(BONUS)和薪资等级(SALGRADE)表的完整REST API
- 实时日志文件监控功能，支持WebSocket实时更新
- 可配置的监控参数（监控文件路径、更新间隔等）
- 简洁美观的日志监控界面
- 支持SQLite数据库，设计兼容Oracle

## 技术栈

- **后端**：Flask, SQLAlchemy, Flask-SocketIO
- **数据库**：SQLite (可迁移至Oracle)
- **通信**：RESTful API, WebSocket, Server-Sent Events
- **工具**：Flask-Migrate, Blueprint, Eventlet

## 安装

1. 克隆仓库
```bash
git clone https://github.com/yourusername/db-tool-server.git
cd db-tool-server
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 初始化数据库
```bash
flask db upgrade
```

## 配置

主要配置在`config/config.py`文件中，你可以通过环境变量或直接修改配置文件来自定义配置：

```python
# 数据库配置
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(BASE_DIR, 'db_tool.db')

# 日志监控配置
LOG_MONITOR_FILE = os.environ.get('LOG_MONITOR_FILE') or '/var/log/system.log'  # 默认监控的日志文件
LOG_MONITOR_MAX_LINES = int(os.environ.get('LOG_MONITOR_MAX_LINES') or 1000)    # 最大显示行数
LOG_MONITOR_UPDATE_INTERVAL = int(os.environ.get('LOG_MONITOR_UPDATE_INTERVAL') or 5)  # 更新间隔(秒)
```

## 运行

启动服务器：
```bash
python run.py
```

服务器默认运行在 `http://localhost:5001`

## API 接口

### 部门管理 (DEPT)

- `GET /api/dept/` - 获取所有部门
- `GET /api/dept/<deptno>` - 获取指定部门信息
- `POST /api/dept/` - 创建新部门
- `PUT /api/dept/<deptno>` - 更新部门信息
- `DELETE /api/dept/<deptno>` - 删除部门

### 员工管理 (EMP)

- `GET /api/emp/` - 获取所有员工
- `GET /api/emp/<empno>` - 获取指定员工信息
- `GET /api/emp/dept/<deptno>` - 获取某部门的所有员工
- `GET /api/emp/job/<job>` - 获取指定职位的所有员工
- `POST /api/emp/` - 创建新员工
- `PUT /api/emp/<empno>` - 更新员工信息
- `DELETE /api/emp/<empno>` - 删除员工

### 奖金管理 (BONUS)

- `GET /api/bonus/` - 获取所有奖金记录
- `GET /api/bonus/ename/<ename>` - 获取某员工的奖金记录
- `GET /api/bonus/job/<job>` - 获取某职位的奖金记录
- `POST /api/bonus/` - 创建奖金记录
- `PUT /api/bonus/<id>` - 更新奖金记录
- `DELETE /api/bonus/<id>` - 删除奖金记录

### 薪资等级管理 (SALGRADE)

- `GET /api/salgrade/` - 获取所有薪资等级
- `GET /api/salgrade/<grade>` - 获取指定等级的薪资范围
- `GET /api/salgrade/sal/<sal>` - 根据薪资获取对应等级
- `POST /api/salgrade/` - 创建薪资等级
- `PUT /api/salgrade/<grade>` - 更新薪资等级
- `DELETE /api/salgrade/<grade>` - 删除薪资等级

### 日志监控

- `GET /api/log/` - 获取日志内容
- `GET /api/log/stream` - 流式获取日志更新（Server-Sent Events）
- `GET /api/log/info` - 获取日志文件信息
- `GET /logs` - 日志监控Web界面

## 日志监控功能

该项目包含一个实时日志监控系统，可以监控服务器上的日志文件并通过Web界面实时显示。

主要特点：
- 实时监控指定日志文件的变化
- 支持WebSocket实时推送日志更新
- 可配置的监控参数（显示行数、更新间隔等）
- 美观的监控界面，支持下载日志、滚动控制等功能

## 迁移到Oracle (TODO...)

项目最初基于SQLite开发，但设计上兼容Oracle数据库。迁移步骤：

1. 修改配置文件中的数据库连接字符串：
```python
SQLALCHEMY_DATABASE_URI = 'oracle://username:password@hostname:port/sid'
```

2. 安装Oracle数据库驱动：
```bash
pip install cx_Oracle
```

3. 运行数据库迁移：
```bash
flask db migrate
flask db upgrade
```

## 项目结构

```
db-tool-server/
├── app/                      # 应用主目录
│   ├── api/                  # API接口
│   ├── models/               # 数据模型
│   ├── templates/            # 模板文件
│   ├── utils/                # 工具函数
│   ├── __init__.py           # 应用初始化
│   ├── routes.py             # 页面路由
│   └── socket_events.py      # WebSocket事件处理
├── config/                   # 配置文件
│   ├── config.py             # 主配置
│   └── db/                   # 数据库脚本
├── migrations/               # 数据库迁移文件
├── venv/                     # 虚拟环境
├── .gitignore                # Git忽略文件
├── README.md                 # 项目说明
├── requirements.txt          # 依赖列表
└── run.py                    # 运行脚本
```

## 许可证

[MIT License](LICENSE) 