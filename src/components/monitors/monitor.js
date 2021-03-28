import React from "react";
import { Redirect } from "react-router-dom";
import request from "../../utils/request";
import Button from "react-bootstrap/Button";
import "./monitor.css";

export default function Monitor({ monitor }) {
  if (!monitor.log) {
    monitor.log = {};
  }
  return (
    <div class="list-group list-group-flush border-bottom scrollarea white">
      <div class="card proj-progress-card">
        <div class="card-block">
          <div class="row">
            <div class="col-xl-3 col-md-6">
              <h6>{monitor.name}</h6>
              <h5 class="m-b-30 f-w-700">
                {monitor.request_count}<span class="text-c-green m-l-10">{monitor.successful_percent}%</span>
              </h5>
              <div class="progress">
                <div
                  class="progress-bar bg-success"
                  style={{ width: (monitor.successful_percent ?  monitor.successful_percent: 0) + "%" }}
                ></div>
                {(monitor.successful_percent || monitor.successful_percent ==0 ) ? (
                                    <div
                                    class="progress-bar bg-danger"
                                    style={{ width: (100 - monitor.successful_percent) + "%" }}
                                  ></div>
                )
                  :
                  ('')
              
              }
              </div>
            </div>
            <div class="col-xl-3 col-md-6">
              URL: {monitor.url}
              </div>
              <div class="col-xl-3 col-md-6">
              Last request {monitor.log.response_code || monitor.log.error}
              </div>
              <div class="col-xl-3 col-md-6">
              Time {parseFloat(monitor.log.response_time).toFixed(2)}s
              </div>
          </div>
        </div>
      </div>
    </div>
  );
}
