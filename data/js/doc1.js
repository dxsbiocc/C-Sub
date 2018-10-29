function test1() {
    var myhref = document.getElementById("a1");
    alert(myhref.innerText);
}

//通过名称来获取对象（元素）
function test2() {
    var hobbies = document.getElementsByName("hobby");
    for(var i = 0; i < hobbies.length; i++){
        if(hobbies[i].checked){
            alert("你的爱好是：" + hobbies[i].value);
        }
    }
}

//通过标签名来获取对象（元素）
function test3() {
    var ipt = document.getElementsByTagName("input");
    for(var i = 0; i < ipt.length; i++){
        alert(ipt[i].value);
    }
}

//创建元素
function test4() {
    //create
    var myele = document.createElement("a");
    //add nessary information
    myele.href = "http://www.baidu.com";
    myele.innerText = "链接到百度";
    myele.id = "id1"
    // myele.style.left = "200px";
    // myele.style.top = "300px";
    // myele.style.position = "absolute";
    //add to document.body
    //document.body.appendChild(myele);
    //将元素放入div中
    document.getElementById("div1").appendChild(myele);
}

//delete element, must be know that parent element
function test5() {
    //method 1
    // document.getElementById("div1").removeChild(document.getElementById('id1'));
    //method 2
    document.getElementById("id1").parentNode.removeChild(document.getElementById('id1'));
    // alert(document.getElementById("id1").parentNode.id);
}