import { Injectable, Component, Input, EventEmitter } from '@angular/core';
import { DbService } from './db.service';
import { Proxy } from '../proxy.service';

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

    constructor(private dbService: DbService, private proxyService: Proxy) {
        this.proxyService.subscribeDbs((v: string[]) => {
            this.dbs = v;
        });
        this.proxyService.subscribeTables((v: string[]) => {
            this.tables = v;
        });
    }

    private onChange(event, str) {
        console.log(str);
        this.proxyService.notifyDbSelected(str);
    }
}
