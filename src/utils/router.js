import React from 'react';
import { Route, Redirect } from "react-router-dom";

// const ProtectedRoute = ({ component: Component, auth, ...rest }) => (
//     <Route {...rest} render={(props) => (auth === true ? <Component {...props} /> : <Redirect to='/login' />)} />
// )


function ProtectedRoute({ children, auth, ...rest}) {
  return (
    <Route
      {...rest}
      render={({ location }) =>
        auth ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: location }
            }}
          />
        )
      }
    />
  );
}


export default ProtectedRoute;