import React from 'react'
import {Redirect} from 'react-router-dom'

export default function MainPage({auth}){

  // let [user, setUser] = React.useState({})
  // let [is_authorized, setAuthBool] = React.useState(null)
    console.log(auth === true)
    return (
      <div>
      {auth === true ? (
        <Redirect to='/dashboard' />)
        :
        ('')
      }
      </div>
    )


}