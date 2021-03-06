doc_desc = """
## 介接協定
- API 介接方式採用 HTTP 協定，以 GET 或 POST 方式傳遞參數，文字編碼為 UTF-8 。 

## API 路徑說明 
- [ ApiRootPath ] = [ DomainName ] + [ RootPath ]= investment-sheet.conquers.co /investment_sheet/api/v1 
    - [ DomainName ] = investment-sheet.conquers.co（ 網域 ） 
    - [ RootPath ] = / investment_sheet /api/v1（ 專案名稱/api/版本號 ） 

- Example：Login API -> [ ApiRootPath ]/login = http://investment-sheet.conquers.co /investment_sheet/api/v1/login 

## 請求方式 

- 指定 RESTful 的 HTTP Request Method 包含但不限於下列四個方式： 
    - GET ： 從伺服器取出資源（一項或多項） 
    - POST ： 在伺服器新建一個資源 
    - PUT ： 在伺服器更新資源 
    - DELETE ： 從伺服器刪除資源 

## 伺服器端參數設定 
- 限制 
    - upload_max_filesize = 10M 
    - post_max_size = 10M   




## Status Code

<table class="parameters table table-bordered table-striped">
    <thead>
    <tr>
        <th>ERROR CODE</th>
        <th>描述</th>
        <th>備註</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>200</td>
        <td>Success</td>
        <td>操作成功</td>
    </tr>
    <tr>
        <td>201</td>
        <td>Success</td>
        <td>成功創立資料</td>
    </tr>
    <tr>
        <td>204 (軟刪除 response 200) </td>
        <td>No Content</td>
        <td>刪除資料成功</td>
    </tr>
    <tr>
        <td>400</td>
        <td>Bad Request</td>
        <td>操作失敗(驗證或參數格式等錯誤，註冊失敗等都會出現在這邊)</td>
    </tr>
    <tr>
        <td>401</td>
        <td>Unauthorized</td>
        <td>驗證沒有通過</td>
    </tr>
    <tr>
        <td>403</td>
        <td>Forbidden</td>
        <td>禁止訪問，權限禁止</td>
    </tr>
    <tr>
        <td>404</td>
        <td>Not Found</td>
        <td>沒有發現該資源</td>
    </tr>
    <tr>
        <td>405</td>
        <td>Method Not Allowed</td>
        <td>請求錯誤 (GET, POST) 等錯誤</td>
    </tr>
    <tr>
        <td>500</td>
        <td>Internal Server Error</td>
        <td>Server 出問題</td>
    </tr>
    </tbody>
</table>

"""
