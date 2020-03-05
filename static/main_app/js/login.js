function changeForm(v)
{
    if (v == 0) {
        document.getElementById("registerForm").className += " active";
        document.getElementById("loginForm").className = "fieldset-button";
        document.getElementById("login").hidden = true;
        document.getElementById("register").hidden = false;
    } else if (v == 1) {
        document.getElementById("registerForm").className = "fieldset-button";
        document.getElementById("loginForm").className += " active";
        document.getElementById("login").hidden = false;
        document.getElementById("register").hidden = true;
    }
}

function showPassword(id)
{
      var x = document.getElementById(id);
      var icon = document.getElementById(id + "Icon");
  if (x.type === "password") {
    x.type = "text";
    icon.className = "fa fa-eye-slash icon";
  } else {
    x.type = "password";
    icon.className = "fa fa-eye icon";
  }
}