import axios from "axios";

export interface CreateEvent {
  title: string;
  start: number;
  end: number;
  allDay: boolean;
}


export interface CalendarEvent {
  id: string;
  title: string;
  start: number;
  end: number;
  allDay: boolean;
}

interface GetEvents {
  items: CalendarEvent[]
}

interface DeleteEvent {
  success: boolean
}

export class EventService {
  async getEvents(): Promise<GetEvents> {
    const { data } = await axios.get<GetEvents>(
      "http://localhost:5001/api/v1/events"
    );
    return data;
  }
  async createEvent(event: CreateEvent): Promise<CalendarEvent> {
    const copy = new Date(event.start);
    copy.setTime(event.start - copy.getTimezoneOffset() * 60 * 1000); // TODO: This assumes the offset is negative. Fix later.
    // @ts-expect-error type cast to string
    event.start = copy.toISOString();
    const { data } = await axios.post<CalendarEvent>(
      "http://localhost:5001/api/v1/events",
      event
    );
    return data;
  }
  async updateEvent(event: CalendarEvent): Promise<CalendarEvent> {
    const { data } = await axios.put<CalendarEvent>(
      `http://localhost:5001/api/v1/events/${event.id}`,
      event
    );
    return data;
  }
  async deleteEvent(id: string): Promise<DeleteEvent> {
    const { data } = await axios.delete<DeleteEvent>(
      `http://localhost:5001/api/v1/events/${id}`
    );
    return data;
  }
}
