import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { DbLoginComponent } from './db/db-login.component';
import { DbsComponent } from './db/dbs.component';
import { DbService } from './db/db.service';

@NgModule({
  declarations: [
    AppComponent,
    DbLoginComponent,
    DbsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [DbService],
  bootstrap: [AppComponent]
})
export class AppModule { }
