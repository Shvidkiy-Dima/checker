import React from 'react';
import { Redirect, Route, Switch} from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import {Routes} from "./enums/routes.enum";
import {RootState} from "./store/rootReducer";
import {getProfileAction} from './store/actions/profile'
import Login from './pages/login'
import Dashboard from "./pages/dashboard";
import DetailMonitor from "./pages/monitor";
import Registration from "./pages/registration";

function App() {

  const dispatch = useDispatch()
  const isAuth = useSelector((state: RootState) => state.profile.isAuth);

  React.useEffect(()=>{
    dispatch(getProfileAction())
  }, [isAuth])

  if (isAuth === null) {
    return null
  }


  if (isAuth === false) {
		return (
                <Switch>
                    <Route exact={true} path={`/${Routes.Login}`}  component={Login}/>;
                    <Route exact={true} path={`/${Routes.Registration}`}  component={Registration}/>;
                    <Redirect to={`/${Routes.Login}`} />
                </Switch>
		);
	}




  return (
        <Switch>
            <Route exact={true} path={`/${Routes.Home}`} component={Dashboard}/>
            <Route path={`/${Routes.Monitor}`} component={DetailMonitor}/>
            <Redirect to={`/${Routes.Home}`}/>
        </Switch>
    );

}

export default App;
