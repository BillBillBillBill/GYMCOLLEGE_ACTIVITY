
function AjaxClass() {
    var xmlhttp = null;
    if (window.XMLHttpRequest) {    // code for IE7, Firefox, Opera, etc.
        xmlhttp = new XMLHttpRequest();
        xmlhttp.withCredentials = true;
    } else if (window.ActiveXObject) {    // code for IE6, IE5
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
    } else {
        alert('Your browser does not support XMLHTTP');
    }

    var self = this;
    this.Method = 'POST';
    this.Url = '';
    this.Async = true;
    this.Arg = '';
    this.CallBack = function() {};
    this.Loading = function() {};
    this.Send = function() {
        if (this.Url === '') {
            return false;
        }
        if (!xmlhttp) {
            return IframePost();
        }

        xmlhttp.open(this.Method, this.Url, this.Async);
        xmlhttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        // xmlhttp.setRequestHeader("Access-Control-Allow-Credentials", 'true');
        // xmlhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState === 4) {
                var Result = false;
                Result = xmlhttp.responseText;
                xmlhttp = null;
                self.CallBack(Result);
            } else {
                self.Loading();
            }
        };

        if (this.Method === 'GET') {
            xmlhttp.send(null);
        } else {
            xmlhttp.send(this.Arg);
        }
    };

    //Iframe方式提交
    function IframePost() {
        var Num = 0;
        var obj = document.createElement('iframe');
        obj.attachEvent('onload', function() {
            self.CallBack(obj.contentWindow.document.body.innerHTML);
            obj.removeNode();
        });
        obj.attachEvent('onreadystatechange', function() {
            if (Num >= 5) {
                alert(false);
                obj.removeNode();
            }
        });
        obj.src = self.Url;
        obj.style.display = 'none';
        document.body.appendChild(obj);
    }
}

var sendajax = function (method, url, data, cb) {
    var Ajax = new AjaxClass();         // 创建AJAX对象
    Ajax.Method = method;
    Ajax.Url = url;
    Ajax.Arg = data;
    Ajax.Async = true;                   // 是否异步
    Ajax.Loading = function() {          //等待函数
        console.log('Sending...');
    };
    // 回调函数
    if (cb) {
        Ajax.CallBack = cb;
    } else {
        Ajax.CallBack = function(ret) {
            console.log('Response:', ret);
        };
    }

    Ajax.Send();                        // 发送请求
};