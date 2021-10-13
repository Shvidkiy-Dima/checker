import {ThunkAction} from 'redux-thunk'
import {RootState} from '../rootReducer'
import {TProfileAction} from "../../interfaces/profile";
import {ApiGetProfile} from '../../api/profile'
import {ApiLogout} from "../../api/auth";
import {EProfileActions} from "../../enums/actions.enum";
import WebSocketConnection from '../../utils/ws'

export const SetProfileAction = (payload: any): any => ({
	type: EProfileActions.SetProfile,
	payload,
});


export const SetTelegramAction = (payload: boolean): any => ({
	type: EProfileActions.SetTelegram,
	payload,
});

export const LogoutAction = (): TGetProfileAction =>
	async (dispatch, getState) => {
		await ApiLogout()
		localStorage.removeItem('token');
		const ws = getState().profile.ws
		ws.close()

		dispatch({
			type: EProfileActions.Logout
			})

	}

export const getProfileAction = (): TGetProfileAction =>
	async (dispatch, getState) => {
		const state = getState()
		let ws: WebSocketConnection | null = state.profile.ws
		if (localStorage.token) {
			try {
				const {data} = await ApiGetProfile();
				ws = new WebSocketConnection()
				ws.connect('ws/dashboard/')
				dispatch(SetProfileAction({...data, ws}));

			} catch (error) {
				if (ws !== null && ws.connected) ws.close()
				console.error(error);
				dispatch(SetProfileAction({ isAuth: false, ws: null}));
			}
		} else {
			if (ws !== null && ws.connected) ws.close()
			dispatch(SetProfileAction({ isAuth: false, ws: null}));
		}
	};

type TGetProfileAction = ThunkAction<Promise<void>, RootState, unknown, TProfileAction>;