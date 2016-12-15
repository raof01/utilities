import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule }  from "@ngrx/store-devtools";
import { DbReducer } from './reducers/db.reducers';
import { environment } from '../../environments/environment';

// todo: Move trajectory table reducer to the trajectory-table ngmodule once ngrx/store supports that functionality
export const APP_STORES: any[] = [
    StoreModule.provideStore({
        dbReducer: DbReducer
    })
];

if (!environment.production) {
    APP_STORES.push(StoreDevtoolsModule.instrumentStore());
}
