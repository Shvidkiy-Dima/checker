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
  const [isAutheticated, setisAutheticated] = React.useState(null);
  const [User, setUser] = React.useState(null);

  function login() {
    getUser()
  }

  function logout() {
    localStorage.removeItem("token")
    setisAutheticated(false);
    setUser(null)
    ws.close()
  }

  function getUser() {
    request(
      { method: "get", url: "api/account/profile/" },
      (res) => {
        setUser(res.data);
        setisAutheticated(true);
        ws.connect('ws/dashboard/')
      },
      (err) => {
        setisAutheticated(false);
        ws.close()
      }
    );
  }

  React.useEffect(getUser, []);

  if (isAutheticated === null){
    return null
  }

  return (
    <Router history={customHistory}>
      <Switch>
        <Route exact path="/registration">
          <RegForm auth={isAutheticated} />
        </Route>

        <Route exact path="/login">
          <LoginForm auth={isAutheticated} login={login} />
        </Route>

        <ProtectedRoute path="/dashboard" auth={isAutheticated}>
          <DashBoard user={User} logout={logout} ws={ws}/>
        </ProtectedRoute>

        <Route exact path="/">
          <MainPage auth={isAutheticated} />
        </Route>
      </Switch>
    </Router>

  );
}

export default App;


