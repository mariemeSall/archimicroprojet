import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PopupService {

  constructor() { }

  makePopUp(data: any) {
    return `` +
      `<div>IP: ${ data.ip }</div>` +
      `<div>Date: ${ data.date }</div>`
  }
}
