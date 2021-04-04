import React from "react";
import {
  HashRouter as Router,
  Switch,
  Route,
  Link,
  useParams,
  useRouteMatch,
} from "react-router-dom";
import {FormCheck} from "react-bootstrap";
import request from "../../utils/request";


export default function Config() {
  
    const [Telegram, SetTelegram] = React.useState(false)
    const [TelegramLink, SetTelegramLink] = React.useState(null)

    function GetTelegram(){

        request({url: 'api/config/', method: 'patch', data: {'enable_telegram': !Telegram}},
        (res)=>{
            let is_enabled = res.data['enable_telegram']
            SetTelegram(is_enabled)
            if (is_enabled){
                request({url: 'api/notification/telegram/', method: 'post'},
                (res)=>{
                    let link = res.data['deeplink']
                    SetTelegramLink(link)
                },
                (err)=>{
                    
                })
            }

        },
        (err)=>{})
    }

  return (
    <div>
      <div class="container-fluid">
        <div class="row">
          <div class="col-3 p-3 text-white bg-dark" style={{ width: "280px" }}>
            <svg class="bi me-2" width="40" height="32"></svg>
            <hr />
            <ul class="nav nav-pills flex-column mb-auto">
              <li class="nav-item">
                <a href="#" class="nav-link text-white">
                  <svg class="bi me-2" width="16" height="16"></svg>
                  <Link to="/dashboard">Dashboard</Link>
                </a>
              </li>
              <li>
                <a href="#" class="nav-link active">
                  <svg class="bi me-2" width="16" height="16"></svg>
                  Settings
                </a>
              </li>
            </ul>
            <hr />
          </div>
          <div class="col-9">
            <div class="list-group list-group-flush border-bottom scrollarea">
              <div class="card proj-progress-card">
                <div class="card-block">
                <FormCheck custom type="switch">
        <FormCheck.Input isInvalid checked={Telegram} />
        <FormCheck.Label onClick={GetTelegram}>
          Enable Telegram Notificaton
        </FormCheck.Label>
      </FormCheck>
                {TelegramLink ? 
                (<a href={TelegramLink}>{TelegramLink}</a>)
                :
                ('')}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
