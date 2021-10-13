import {EProfileActions} from '../../enums/actions.enum';
import {TProfileAction} from '../../interfaces/profile';

const initState: any = {
	isAuth: null,
	has_telegram: null,
	user_id:null,
	email: null,
	ws: null
};

const initialState = { ...initState };

export const profileReducer = (state = initialState, action: TProfileAction) => {
	switch (action.type) {
		case EProfileActions.SetProfile:
			console.log(action)
			return {
				...state,
				isAuth: true,
				...action.payload,
				};
		case EProfileActions.SetTelegram:
			return {
				...state,
				has_telegram: true,
				};

		case EProfileActions.Logout:
			return {
				...state,
				isAuth: false
			}
		default:
			return state;
	}
};
