import type { AvatarProps } from '@nuxt/ui'

export type UserStatus = 'subscribed' | 'unsubscribed' | 'bounced'
export type SaleStatus = 'paid' | 'failed' | 'refunded'

export interface User {
  id: number
  name: string
  email: string
  avatar?: AvatarProps
  status: UserStatus
  location: string
}

export interface Sender {
  name: string
  email?: string
  avatar?: AvatarProps
}

export interface Mail {
  id: number
  unread?: boolean
  from: Sender
  subject: string
  body: string
  date: string
}

export interface Member {
  name: string
  username: string
  role: 'member' | 'owner'
  avatar: AvatarProps
}

export interface Stat {
  title: string
  icon: string
  value: number | string
  variation: number
  formatter?: (value: number) => string
}

export interface Sale {
  id: string
  date: string
  status: SaleStatus
  email: string
  amount: number
}

export interface Notification {
  id: number
  unread?: boolean
  sender: Sender
  body: string
  date: string
}

export type Period = 'daily' | 'weekly' | 'monthly'

export interface Range {
  start: Date
  end: Date
}

export interface ScheduleActivity {
  /** General schedule id (`study_year.general_schedules.id`) */
  id: string
  /** Color indicator of the schedule activity type (e.g. `#10b981`) */
  color: string
  /** Display name of the schedule activity type */
  activityTypeName: string
  name: string
  /** `yyyy-MM-ddTHH:mm` */
  startAt: string
  /** `yyyy-MM-ddTHH:mm` */
  endAt?: string
  /** Whether attendance is taken for this activity (backend: `is_attendence_check`) */
  isAttendenceCheck: boolean
}

export interface ScheduleRow {
  /** `yyyy-MM` — used for month grouping */
  monthKey: string
  dayName: string
  /** `dd-MM-yyyy` */
  date: string
  activities: ScheduleActivity[]
}

export interface GradeScheduleActivity {
  /** Grade schedule id (`study_year.grade_schedules.id`) */
  id: string
  /** Linked general schedule id (`study_year.general_schedules.id`), if any */
  generalScheduleId: string | null
  /** Color indicator of the schedule activity type (e.g. `#10b981`) */
  color: string
  /** Display name of the schedule activity type */
  activityTypeName: string
  name: string
  /** `yyyy-MM-ddTHH:mm` */
  startAt: string
  /** `yyyy-MM-ddTHH:mm` */
  endAt?: string
  /** Whether attendance is taken for this activity (backend: `is_attendence_check`) */
  isAttendenceCheck: boolean
}

export interface GradeScheduleRow {
  /** `yyyy-MM` — used for month grouping */
  monthKey: string
  dayName: string
  /** `dd-MM-yyyy` */
  date: string
  activities: GradeScheduleActivity[]
}
