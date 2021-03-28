import React from 'react'
import {Redirect} from 'react-router-dom'
import {InputHook} from '../../utils/hooks'
import axios from 'axios'


export default function RegForm({auth}){

    return (
        <div>
        {auth === true ? (
          <Redirect to='/dashboard' />)
          :
          (<div>
  
              <p>Reg</p>
  
          </div>)
        }
        </div>
      )

}