import {ApiGetMonitor} from "../../api/monitor";
import {EMonitorActions} from "../../enums/actions.enum";
import {ThunkAction} from "redux-thunk";
import {RootState} from "../rootReducer";
import {TMonitorAction} from "../../interfaces/monitor";
import {convert_for_bar, convert_for_table, convert_for_chart} from "../../utils/funcs";

export const getMonitorAction = (id: string): TMonitorActionThunk =>
	async (dispatch) => {
		try {
			const {data} = await ApiGetMonitor(id)
			const bar_data = convert_for_bar(data.log_groups)
			const chart_data = convert_for_chart(data.interval_logs)
			const table_data = convert_for_table(data.last_error_logs)

			dispatch({
				type: EMonitorActions.SetMonitor,
				payload: {...data, bar_data, chart_data, table_data}
			})
		}
		catch {
			dispatch({
				type: EMonitorActions.SetNotFound,
				payload: true
			})

		}

};


type TMonitorActionThunk = ThunkAction<Promise<void>, RootState, unknown, TMonitorAction>;