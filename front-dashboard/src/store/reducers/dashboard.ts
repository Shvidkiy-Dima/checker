import {EDashboardActions} from '../../enums/actions.enum';
import {
	IResponseMonitor,
	TMonitorsAction,
	TResponseMonitors
} from '../../interfaces/dashboard';


const initState: any = {
	monitors: [],
	ShowModal: false
};

const initialState =  {...initState};




export const DashboardReducer = (state = initialState, action: TMonitorsAction) => {

	let monitor: IResponseMonitor
	let monitor_id: string
	let monitors: TResponseMonitors
	let index: number

	switch (action.type) {

		case EDashboardActions.SetMonitors:
			  return {
				  ...state,
				  monitors: action.payload,
			  }

		case EDashboardActions.UpdateMonitor:
			monitor = action.payload
			monitors = [...state.monitors]
			index = monitors.findIndex((m)=>m.id===monitor.id)
			monitors[index] = monitor
			return {
				...state,
				monitors: monitors
			}

		case EDashboardActions.AddMonitor:
			return {
				...state,
				ShowModal: false,
				monitors: [...state.monitors, action.payload]
			}
		case EDashboardActions.ShowModal:
			return {
				...state,
				ShowModal: action.payload
			}

		case EDashboardActions.DeleteMonitor:
			monitor_id = action.payload
			monitors = [...state.monitors]
			index = monitors.findIndex((m)=>m.id===monitor_id)
			monitors.splice(index, 1)
			return {
				...state,
				monitors: [...monitors],
			}

		default:
			return state;
	}
};
