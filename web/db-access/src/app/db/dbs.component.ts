import { Injectable, Component, Input } from '@angular/core';

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
}
