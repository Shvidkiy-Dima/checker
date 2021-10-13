import React from "react";
import "../dashboard/dashboard.css";
import { Tooltip } from "antd";
import Moment from 'moment'


export default function MultiColorProgressBar({monitor}: {monitor: any}) {
  const [Start, SetStart] = React.useState("");
  const [End, SetEnd] = React.useState("");
  const [ResCode, setResCode] = React.useState("");
  const [ResError, setResErro] = React.useState(null);

  const readings = monitor.bar_data

  function MakeBar(readings: Array<any>){
      return readings.map((item, i) => {
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
            />
          );
      });
  }

  let bars = React.useMemo(()=>MakeBar(readings), [monitor.last_log.created])

  let first: any = bars[0]
  let last: any = bars[bars.length-1]

  if (first){
    first = Moment.utc(first.created).local().format("MM/DD/HH:mm:ss")
    last = Moment.utc(last.created).local().format("MM/DD/HH:mm:ss")
  }

  return (
    <div className="multicolor-bar">
      <Tooltip
        title={
          <div>
            <p>Start: {Moment.utc(Start).local().format("MM/DD/HH:mm:ss")}</p>
            <p>End: {End ? Moment.utc(End).local().format("MM/DD/HH:mm:ss"): ''}</p>
            <p>Response code: {ResCode}</p>
    w        <p>Error: {ResError}</p>
          </div>
        }
      >
        <div className="bars">{bars}</div>
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