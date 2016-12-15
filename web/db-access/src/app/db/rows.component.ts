import { Injectable, Component, Input } from '@angular/core';
import { DbProxy } from './db.proxy';

@Component({
    selector: 'rows',
    templateUrl: '../html/rows.component.html',
    styleUrls: ['../styles/app.component.css']
})

@Injectable()
export class RowsComponent {
    @Input()
    rows: any = undefined;
    private fields: string[] = undefined;

    constructor(private proxy: DbProxy) {
        this.proxy.subscribeFields(this.onFieldsReceived.bind(this));
        this.proxy.subscribeRows(this.onRowsReceived.bind(this));
    }

    private onRowsReceived(v: any[]) {
        this.rows = v;
    }

    private onFieldsReceived(v: string[]) {
        this.fields = v;
    }
}
