### 使用技术栈：
python, django, celery

### 笔试题目：
1. 设计一个图书馆管理系统，维护图书相关的属性
    http://127.0.0.1:8000/admin/library/book/ 维护图书相关属性

2. 提供图书的查询、录入、修改和销毁的 API
    查询：get   http://127.0.0.1:8000/api/books/
    录入：post  http://127.0.0.1:8000/api/books/
    修改：put   http://127.0.0.1:8000/api/books/{id}/
    销毁：delete   http://127.0.0.1:8000/api/books/{id}/

3. 提供借书、还书的 API
    借书：post  http://127.0.0.1:8000/api/borrow-records/
    还书：put   http://127.0.0.1:8000/api/borrow-records/{id}/

4. 图书借阅期限为 30 天，每天 08:00 发通知将在 7 天内到期的图书借阅者，提醒还书
    celery -A library_management beat --loglevel=info
5. 实现一个中间件，记录每个 API 请求的参数和耗时
    celery -A library_management worker --loglevel=info
### 提交方式：
1. 使用 git 提交代码到 github 或者 gitee，提供对应代码仓库的地址。