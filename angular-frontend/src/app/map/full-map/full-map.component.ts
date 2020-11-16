import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-full-map',
  templateUrl: './full-map.component.html',
  styleUrls: ['./full-map.component.scss']
})
export class FullMapComponent implements OnInit {
  width;
  constructor() { }

  ngOnInit(): void {
    this.width = screen.width;
  }

}