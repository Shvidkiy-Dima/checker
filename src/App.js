import React from "react";
import {
  HashRouter as Router,
  Switch,
  Link,
  Route,
  Redirect,
} from "react-router-dom";
import LoginForm from "./components/auth/login_form";
import RegForm from "./components/auth/reg_form";
import MainPage from "./components/main_page/main";
import DashBoard from "./components/monitors/dashboard";
import ProtectedRoute from "./utils/router";
import request from "./utils/request";
import ws from './utils/ws'
import './App.css'
import { createBrowserHistory } from "history";


const customHistory = createBrowserHistory();


function App() {
  const [isAutheticated, setisAutheticated] = React.useState(false);
  const [User, setUser] = React.useState({});

  function login() {
    setisAutheticated(true);
  }

  function logout() {
    setisAutheticated(false);
  }

  function get_user() {
    request(
      { method: "get", url: "api/account/profile/" },
      (res) => {
        setUser(res.data);
        setisAutheticated(true);
      },
      (err) => {
        setisAutheticated(false);
      }
    );
  }


  function ConnectToWs(){ 
    if (isAutheticated){
      ws.connect('ws/dashboard/')
   }
   else {
       ws.close()
   }
  }

  React.useEffect(ConnectToWs, [isAutheticated])
  React.useEffect(get_user, [isAutheticated]);

  return (
    <Router history={customHistory}>
      <Switch>
        <Route exact path="/registration">
          <RegForm auth={isAutheticated} />
        </Route>

        <Route exact path="/login">
          <LoginForm auth={isAutheticated} login={login} />
        </Route>

        <Route path="/dashboard">
          <DashBoard user={User} logout={logout} ws={ws}/>
        </Route>

        <Route exact path="/">
          <MainPage auth={isAutheticated} />
        </Route>
      </Switch>
    </Router>

  );
}

export default App;


