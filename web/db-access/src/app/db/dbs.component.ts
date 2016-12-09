import { Injectable, Component, Input, EventEmitter } from '@angular/core';
import { DbService } from './db.service';
import { HubService } from '../hub.service';

@Component({
    selector: 'dbs',
    templateUrl: './dbs.component.html',
    styleUrls: ['../app.component.css']
})

/*
 * NOTE:
 * TODO: db-access logic should be in server side, instead of client side
 */
@Injectable()
export class DbsComponent {
    @Input()
    dbs: string[] = undefined;
    tables: string[] = undefined;

    constructor(private dbService: DbService, private hubService: HubService) {
        this.hubService.subscribeDbs((v: string[]) => {
            this.dbs = v;
        });
        this.hubService.subscribeTables((v: string[]) => {
            this.tables = v;
        });
    }

    private onChange(event, str) {
        console.log(str);
        this.hubService.notifyDbSelected(str);
    }
}
