import React from "react";
import "./monitor.css";
import { Tooltip } from "antd";
import Moment from "react-moment";
import Moment_f from 'moment'


export default function MultiColorProgressBar({ readings, monitor }) {
  const [Start, SetStart] = React.useState("");
  const [End, SetEnd] = React.useState("");
  const [ResCode, setResCode] = React.useState("");
  const [ResError, setResErro] = React.useState(null);


  function MakeBar(readings){
      return readings.map(function (item, i) {
        if (item.value > 0) {
          return (
            <div
              onMouseEnter={() => {
                SetStart(item["start"]);
                SetEnd(item['end'])
                setResCode(item["res_code"]);
                setResErro(item["error"]);
              }}
              className="bar"
              style={{ backgroundColor: item.color, width: item.value + "%" }}
              key={i}
            ></div>
          );
        }
      });
  }


  let bars = React.useMemo(()=>MakeBar(readings), [monitor.last_log.created])



  let first = ''
  let last = ''

  if (first.length > 0){
    let first = Moment_f.utc(first.created).local().format("MM/DD/HH:mm:ss")
    let last = Moment_f.utc(last.created).local().format("MM/DD/HH:mm:ss")
  }

  return (
    <div className="multicolor-bar">
      <Tooltip
        title={
          <div>
            <p>Start: {Moment_f.utc(Start).local().format("MM/DD/HH:mm:ss")}</p>
            <p>End: {End ? Moment_f.utc(End).local().format("MM/DD/HH:mm:ss"): ''}</p>
            <p>Response code: {ResCode}</p>
            <p>Error: {ResError}</p>
          </div>
        }
      >
        <div className="bars">{bars == "" ? "" : bars}</div>
      </Tooltip>

        <div style={{ display: "inline-flex", justifyContent: 'space-between', width: '100%'}}>
          <div>
          <p style={{color: '#968c8c', fontSize: '0.8em'}}>{first}</p>
          </div>
          <div style={{display: 'inline-flex'}}>
            <div style={{marginRight: '10%'}}>
              <span className="dot" style={{ color: "green" }}>
                ●
              </span>
              <span className="label">{monitor.successful_percent}%</span>
            </div>
            <div className="legend">
              <span className="dot" style={{ color: "red" }}>
                ●
              </span>
              <span className="label">{monitor.unsuccessful_percent}%</span>
            </div>
          </div>
          <div>
          <p style={{color: '#968c8c', fontSize: '0.8em'}}>{last}</p>
          </div>
        </div>
  
    </div>
  );
}
