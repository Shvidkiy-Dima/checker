import {ThunkAction} from 'redux-thunk'
import {RootState} from '../rootReducer'
import {ApiGetMonitors, ApiDisableMonitor, ApiDeleteMonitor} from "../../api/dashboard";
import {TMonitorsAction} from "../../interfaces/dashboard";
import {EDashboardActions} from "../../enums/actions.enum";
import {TResponseMonitors} from "../../interfaces/dashboard";
import {IResponseMonitor} from "../../interfaces/dashboard";


const setMonitorsAction = (payload: TResponseMonitors): any => ({
	type: EDashboardActions.SetMonitors,
	payload,
});

const updateMonitorAction = (payload: IResponseMonitor): any => ({
	type: EDashboardActions.UpdateMonitor,
	payload,
});

export const AddMonitorAction = (payload: IResponseMonitor): any => ({
	type: EDashboardActions.AddMonitor,
	payload,
});

export const SetShowModalAction = (payload: boolean): any => ({
	type: EDashboardActions.ShowModal,
	payload
})


export const ShowModalAction = (): TGetMonitorsAction =>
	async (dispatch, getState) => {
		const state = getState()
		dispatch(SetShowModalAction(!state.dashboard.ShowModal))

};



export const getMonitorsAction = (): TGetMonitorsAction =>
	async (dispatch) => {
		const {data} = await ApiGetMonitors()
		dispatch(setMonitorsAction(data))

};

export const deleteMonitorAction = (id: string): TGetMonitorsAction =>
	async (dispatch) => {
		await ApiDeleteMonitor(id)
		dispatch(
			{
				type: EDashboardActions.DeleteMonitor,
				payload: id
			}
		)
};

export const disableMonitorAction = (monitor: IResponseMonitor): TGetMonitorsAction =>
	async (dispatch) => {
		const {data} = await ApiDisableMonitor(monitor.id, !monitor.is_active)
		dispatch(updateMonitorAction({
			...monitor,
			is_active: data.is_active
		}))
};


type TGetMonitorsAction = ThunkAction<Promise<void>, RootState, unknown, TMonitorsAction>;