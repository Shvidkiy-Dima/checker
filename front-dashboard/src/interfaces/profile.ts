import {EProfileActions} from "../enums/actions.enum";

export interface ISetProfileAction {
    payload: Array<any>
    type: EProfileActions.SetProfile

}

export interface ISetTelegramAction {
    payload: any
    type: EProfileActions.SetTelegram
}

export interface ILogoutAction {
    type: EProfileActions.Logout
}


export interface IResponseProfile {
	email: string;
	id: number;
}


export type TProfileAction = ISetProfileAction | ISetTelegramAction | ILogoutAction

