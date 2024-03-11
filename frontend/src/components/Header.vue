<script>
export default {};
</script>
<template>
  <div class="header">
    <div class="wrapper">
      <!--logo-->
      <div class="logo">
        <h1><a href="https://www.baidu.com">舌诊宝</a></h1>
      </div>
      <!--导航nav-->
      <div class="nav">
        <ul>
          <li><a href="https://www.baidu.com">首页</a></li>
          <li><a href="https://www.baidu.com">检测页面</a></li>
          <li><a href="https://www.baidu.com">其他</a></li>
        </ul>
      </div>
      <!--用户user-->
      <div class="user">
        <ul>
          <li><h2><a href="#" class="logo">头像</a></h2></li>
          <li><h2><a href="#">用户user</a></h2></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
/*check page*/
/*版心*/
.wrapper{
  margin: 0 auto;
  width: 1200px;
}

body {
  background-color: #f3f5f7;
}

/*头部区域*/
.header {
  height: 80px;
  background-color: white;
  padding-top: 50px;
}

.header .wrapper {
  display: flex;
}

/*logo*/
.logo a {
  position: relative;
  display: block;
  width: 150px;
  height: 60px;
  bottom: 45px;
  right: 50px;
  background-image: url("../assets/Logo_SZB.png");
  font-size: 0px;
}

/*导航*/
.nav {
  margin-left: 10px;
  position: relative;
  bottom: 40px;
  right: 50px;
}

.nav ul {
  display: flex;
}

.nav li {
  margin: 0 auto;
  list-style: none;
}

.nav li a {
  margin: 10px 50px;
  line-height: 80px;
  background-color: white;
  font-size: 19px;
  color: #181818;
  text-decoration: none;
}

.nav li a:hover {
  border-bottom: 2px solid #00a4ff;
  /*background: #d3d3ca;*/
}

/*用户头像*/
.user {
  display:flex;
  margin: 0 auto;
  position: relative;
  bottom: 40px;
  left: 120px;
}
.user ul {
  margin: auto;
  display: flex;
}
.user ul li {
  display: flex;
  margin: auto;
  list-style: none;
}
.user ul li a {
  margin: auto;
  text-decoration: none;
  font-size: 19px;
  color: #181818;
}
.user ul li a.logo {
  display: block;
  width: 30px;
  height: 30px;
  border-radius: 100%;
  background-image: url("../assets/Chat_Tongue.jpg");
  font-size: 0px;
}
</style>
