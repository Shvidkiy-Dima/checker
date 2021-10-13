import Moment from "moment";

export function convert_for_bar(data: any) {
  let count = 0
  for (let k in data){
    count += data[k]['count']
  }

  let new_data = data.map((e: any) => {
    return {
      start: e.start,
      end: e.end,
      res_code: e.res_code,
      error: e.error,
      value: (100 / count) * e.count,
      color: e.successful ? "green": "#eb4d4b",
    };
  });

  console.log(data)
  console.log(new_data)

  return new_data;
}

export function convert_for_table(data: Array<any>){
  return data.map((i, n)=>({
            key: n,
            created: Moment.utc(i.created).local().format("MM.DD-HH:mm:ss"),
            error: i.error,
            res_code: i.response_code,
            res_time: i.response_time
        })
    )
}


export function convert_for_chart(data: Array<any>){

  const convert_date = (date: string) => Moment.utc(date).local().format("HH:mm:ss")

  const chart_data = data.map((i: any, n, array) =>(
      {
          avg: i.interval_avg,
          date: `${convert_date(i.created)}-${array[n+1] ? convert_date(array[n+1].created): ''}`
      }
      )
  );
  return {
          data: chart_data,
          height: 400,
          xField: "date",
          yField: "avg",
          point: { size: 0.1, shape: "diamond" },
        }
}
