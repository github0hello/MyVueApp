# first 项目

## 项目简介

这是一个使用 Vue 3 构建的OSS工具

## 环境搭建

### 安装依赖

在项目根目录下运行以下命令来安装所需的依赖：

```sh
npm install
```


### 运行

```sh
npm run dev
```

#### 后端

##### Backend

```sh
cd backend
python app.py
```

##### Client
```sh
cd client
python app.py
```

### 要构建生产环境的代码
```sh
npm run build
```

## Note

```
// Create a cookie, valid across the entire site:
Cookies.set('name', 'value');
 
// 创建一个从现在起7天内过期的cookie，在整个站点有效:
Cookies.set('name', 'value', { expires: 7 });
 
// Create an expiring cookie, valid to the path of the current page:
Cookies.set('name', 'value', { expires: 7, path: '' });
 
//           name       value
Cookies.set('TokenKey', token, { expires: 1000, path: '/', domain: 'xx.com' });
 
 
//不写过期时间，默认为1天过期
this.$cookies.set("user_session","25j_7Sl6xDq2Kc3ym0fmrSSk2xV2XkUkX")
 
this.$cookies.set("token","GH1.1.1689020474.1484362313","60s");  // 60秒后过去
 
this.$cookies.set("token","GH1.1.1689020474.1484362313","30MIN");  // 30分钟后过去
```

