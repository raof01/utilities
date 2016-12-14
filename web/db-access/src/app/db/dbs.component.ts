import { Injectable, Component, Input } from '@angular/core';
import { DbService } from './db.service';
import { Proxy } from '../proxy.service';

@Component({
    selector: 'dbs',
    templateUrl: '../html/dbs.component.html',
    styleUrls: ['../styles/app.component.css']
})

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

    private onDbChange(event, str) {
        this.proxyService.notifyDbSelected(str);
    }

    private onTableChange(event, str) {
        this.proxyService.notifyTableSelected(str);
    }
}
