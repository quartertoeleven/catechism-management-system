#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# ///
"""One-time import of 2026-2027 lịch sinh hoạt into current study year.

Usage:
    uv run scripts/import_lich_sinh_hoat.py --token "cms_admin_dashboard=<cookie value>"
    uv run scripts/import_lich_sinh_hoat.py --token "<cookie value>" --dry-run

Token = session cookie copied from logged-in browser (DevTools > Network >
any dashboard-api request > Request Headers > cookie). Value without "=" is
wrapped as cms_admin_dashboard=<value>.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime

# --- constants -------------------------------------------------------------

TYPE_THANHLE = 1
TYPE_GIAOLY = 2
TYPE_KHAC = 99

SCHEDULES_PATH = "/dashboard-api/general-schedules"
DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_COOKIE_NAME = "cms_admin_dashboard"

SUNDAY_START = "06:30"
SUNDAY_END = "08:00"
GIAOLY_START = "09:00"
GIAOLY_END = None
CONFESSION_START = "08:30"
CONFESSION_END = "10:30"

CONFESSION_PREFIX = "Xưng tội"
FIELD_TRIP_PREFIX = "Học Trại"

# --- schedule data (from plan: lich-sinh-hoat-2026-2027.md) ----------------
# (date, type, name) — name combined per source cell

ENTRIES: list[tuple[str, int, str]] = [
    ("2026-09-13", TYPE_THANHLE, "Chúa Nhật 24 Thường Niên Năm A"),
    ("2026-09-13", TYPE_GIAOLY, "Khai giảng GL, Nhận lớp GL"),
    ("2026-09-20", TYPE_THANHLE, "Chúa Nhật 25 Thường Niên Năm A"),
    ("2026-09-20", TYPE_GIAOLY, "Sinh hoạt đầu năm, Gặp Gỡ 1"),
    ("2026-09-24", TYPE_THANHLE, "Thứ Năm, Lễ Trung Thu (Văn nghệ + Phát quà)"),
    ("2026-09-25", TYPE_KHAC, "Thứ Sáu, Đi Lân Quanh Xứ"),
    ("2026-09-27", TYPE_THANHLE, "Chúa Nhật 26 Thường Niên Năm A"),
    ("2026-09-27", TYPE_GIAOLY, "Gặp Gỡ 2 (Mừng BM Sr. Teresina)"),
    (
        "2026-10-04",
        TYPE_THANHLE,
        "Chúa Nhật 27 Thường Niên Năm A, Lễ Mẹ Mân Côi, Chầu Thánh Thể",
    ),
    ("2026-10-04", TYPE_GIAOLY, "Gặp Gỡ 3"),
    (
        "2026-10-11",
        TYPE_THANHLE,
        "Chúa Nhật 28 Thường Niên Năm A, Chào cờ (TT1)",
    ),
    ("2026-10-11", TYPE_GIAOLY, "Gặp Gỡ 4"),
    ("2026-10-18", TYPE_THANHLE, "Chúa Nhật 29 Thường Niên Năm A"),
    ("2026-10-18", TYPE_GIAOLY, "Gặp Gỡ 5"),
    ("2026-10-25", TYPE_THANHLE, "Chúa Nhật 30 Thường Niên Năm A"),
    ("2026-10-25", TYPE_GIAOLY, "Cử hành truyền giáo, Cử hành tháng Mân Côi"),
    ("2026-10-25", TYPE_KHAC, "Xưng tội"),
    (
        "2026-11-01",
        TYPE_THANHLE,
        "Chúa Nhật 31 Thường Niên Năm A, Lễ Các Thánh, Lễ Các Linh Hồn, Chầu Thánh Thể",
    ),
    ("2026-11-01", TYPE_GIAOLY, "Gặp Gỡ 6, Đi viếng nghĩa trang"),
    (
        "2026-11-08",
        TYPE_THANHLE,
        "Chúa Nhật 32 Thường Niên Năm A, Chào cờ (TT2)",
    ),
    ("2026-11-08", TYPE_GIAOLY, "BÀI THU HOẠCH GIAI ĐOẠN 1"),
    ("2026-11-15", TYPE_THANHLE, "Chúa Nhật 33 Thường Niên Năm A"),
    ("2026-11-15", TYPE_GIAOLY, "Gặp Gỡ 7"),
    (
        "2026-11-22",
        TYPE_THANHLE,
        "Chúa Nhật 34 Thường Niên Năm A, Lễ Chúa Kitô Vua",
    ),
    ("2026-11-22", TYPE_GIAOLY, "Gặp Gỡ 8"),
    ("2026-11-29", TYPE_THANHLE, "Chúa Nhật 1 Mùa Vọng"),
    ("2026-11-29", TYPE_GIAOLY, "Gặp Gỡ 9"),
    ("2026-12-06", TYPE_THANHLE, "Chúa Nhật 2 Mùa Vọng, Chầu Thánh Thể"),
    ("2026-12-06", TYPE_GIAOLY, "BÀI THU HOẠCH GIAI ĐOẠN 2"),
    ("2026-12-13", TYPE_THANHLE, "Chúa Nhật 3 Mùa Vọng, Chào cờ (TS1)"),
    ("2026-12-13", TYPE_GIAOLY, "Gặp Gỡ 10"),
    ("2026-12-20", TYPE_THANHLE, "Chúa Nhật 4 Mùa Vọng"),
    ("2026-12-20", TYPE_KHAC, "Xưng tội"),
    ("2026-12-24", TYPE_THANHLE, "Thứ Năm, Lễ Canh Thức Giáng Sinh"),
    ("2026-12-25", TYPE_THANHLE, "Thứ Sáu, Lễ Giáng Sinh"),
    ("2026-12-27", TYPE_THANHLE, "Chúa Nhật Lễ Thánh Gia"),
    ("2026-12-27", TYPE_GIAOLY, "Thi HKI"),
    ("2027-01-01", TYPE_THANHLE, "Thứ Sáu, Lễ Mẹ Thiên Chúa"),
    ("2027-01-03", TYPE_THANHLE, "Chúa Nhật Lễ Hiển Linh, Chầu Thánh Thể"),
    ("2027-01-03", TYPE_GIAOLY, "Gặp Gỡ 11"),
    (
        "2027-01-10",
        TYPE_THANHLE,
        "Chúa Nhật 1 Thường Niên Năm B, Chào cờ (TS2)",
    ),
    ("2027-01-10", TYPE_GIAOLY, "Gặp Gỡ 12"),
    ("2027-01-17", TYPE_THANHLE, "Chúa Nhật 2 Thường Niên Năm B"),
    ("2027-01-17", TYPE_GIAOLY, "Gặp Gỡ 13, Thi Giữa HKII"),
    (
        "2027-01-24",
        TYPE_THANHLE,
        "Chúa Nhật 3 Thường Niên Năm B, Hội Chợ Xuân Đinh Mùi 2027",
    ),
    ("2027-02-06", TYPE_THANHLE, "Thứ Bảy, Tết Nguyên Đán Đinh Mùi 2027"),
    (
        "2027-02-07",
        TYPE_THANHLE,
        "Chúa Nhật 5 Thường Niên Năm B, Chầu Thánh Thể",
    ),
    ("2027-02-10", TYPE_THANHLE, "Thứ Tư, Lễ Tro"),
    ("2027-02-14", TYPE_THANHLE, "Chúa Nhật 1 Mùa Chay, Chào cờ (BĐ1)"),
    ("2027-02-14", TYPE_GIAOLY, "Gặp Gỡ đầu năm"),
    ("2027-02-21", TYPE_THANHLE, "Chúa Nhật 2 Mùa Chay"),
    ("2027-02-21", TYPE_GIAOLY, "Gặp Gỡ 14"),
    ("2027-02-28", TYPE_THANHLE, "Chúa Nhật 3 Mùa Chay"),
    ("2027-02-28", TYPE_GIAOLY, "BÀI THU HOẠCH GIAI ĐOẠN 3"),
    ("2027-03-07", TYPE_THANHLE, "Chúa Nhật 4 Mùa Chay"),
    ("2027-03-07", TYPE_GIAOLY, "ĐANG TRỐNG"),
    ("2027-03-07", TYPE_KHAC, "Xưng tội"),
    (
        "2027-03-14",
        TYPE_THANHLE,
        "Chúa Nhật 5 Mùa Chay, Chào cờ (BĐ2), Chúc mừng BM Cha xứ/Cha phó",
    ),
    ("2027-03-14", TYPE_GIAOLY, "ĐANG TRỐNG"),
    ("2027-03-19", TYPE_THANHLE, "Thứ Sáu, Lễ Thánh Giuse"),
    ("2027-03-21", TYPE_THANHLE, "Chúa Nhật Lễ Lá"),
    ("2027-03-21", TYPE_GIAOLY, "Gặp Gỡ 20"),
    ("2027-03-25", TYPE_THANHLE, "Thứ Năm Tuần Thánh, Lễ Vượt Qua"),
    (
        "2027-03-26",
        TYPE_THANHLE,
        "Thứ Sáu Tuần Thánh, Tưởng Niệm Cuộc Thương Khó Chúa Giêsu",
    ),
    ("2027-03-27", TYPE_THANHLE, "Thứ Bảy Tuần Thánh, Lễ Vọng Phục Sinh"),
    ("2027-03-28", TYPE_THANHLE, "Chúa Nhật 1 Phục Sinh"),
    ("2027-04-04", TYPE_THANHLE, "Chúa Nhật 2 Phục Sinh, Chầu Thánh Thể"),
    ("2027-04-04", TYPE_GIAOLY, "ĐANG TRỐNG"),
    ("2027-04-11", TYPE_THANHLE, "Chúa Nhật 3 Phục Sinh, Chào cờ (BĐ3)"),
    ("2027-04-11", TYPE_GIAOLY, "Chuyên đề 1"),
    ("2027-04-18", TYPE_THANHLE, "Chúa Nhật 4 Phục Sinh"),
    ("2027-04-18", TYPE_GIAOLY, "Chuyên đề 2"),
    ("2027-04-25", TYPE_THANHLE, "Chúa Nhật 5 Phục Sinh"),
    ("2027-04-25", TYPE_GIAOLY, "Chuyên đề 3"),
    ("2027-05-02", TYPE_THANHLE, "Chúa Nhật 6 Phục Sinh, Chầu Thánh Thể"),
    ("2027-05-07", TYPE_KHAC, "Thứ Sáu, GLV Tĩnh Tâm"),
    ("2027-05-08", TYPE_KHAC, "Thứ Bảy, GLV Tĩnh Tâm"),
    (
        "2027-05-09",
        TYPE_THANHLE,
        "Chúa Nhật 7 Phục Sinh, Lễ Chúa Giêsu Lên Trời, Tuyên Hứa Bao Đồng (Dự kiến)",
    ),
    ("2027-05-09", TYPE_KHAC, "Học Trại Buổi 1"),
    ("2027-05-16", TYPE_THANHLE, "Chúa Nhật Lễ Chúa Thánh Thần Hiện Xuống"),
    (
        "2027-05-23",
        TYPE_THANHLE,
        "Chúa Nhật Lễ Chúa Ba Ngôi, Tuyên Hứa Vào Đời (Dự kiến)",
    ),
    ("2027-05-23", TYPE_KHAC, "Học Trại Buổi 2"),
    (
        "2027-05-30",
        TYPE_THANHLE,
        "Chúa Nhật Lễ Mình Máu Chúa, Rước Lễ Lần Đầu (Dự kiến)",
    ),
    ("2027-05-30", TYPE_KHAC, "Học Trại Buổi 3"),
    ("2027-06-06", TYPE_THANHLE, "Chúa Nhật 10 Thường Niên Năm B, Chầu Thánh Thể"),
    ("2027-06-06", TYPE_KHAC, "Học Trại Buổi 4"),
    ("2027-06-10", TYPE_THANHLE, "Thứ Năm, Ban Bí Tích Thêm Sức (Dự kiến)"),
    (
        "2027-06-13",
        TYPE_THANHLE,
        "Chúa Nhật 11 Thường Niên Năm B, Tổng Kết Phát Thưởng",
    ),
    ("2027-06-13", TYPE_KHAC, "Học Trại Buổi 5"),
    ("2027-06-20", TYPE_THANHLE, "Chúa Nhật 12 Thường Niên Năm B"),
    ("2027-06-20", TYPE_KHAC, "Học Trại Buổi 6"),
    ("2027-06-27", TYPE_THANHLE, "Chúa Nhật 13 Thường Niên Năm B"),
    ("2027-06-27", TYPE_KHAC, "Học Trại Buổi 7"),
    ("2027-07-04", TYPE_THANHLE, "Chúa Nhật 14 Thường Niên Năm B, Chầu Thánh Thể"),
    ("2027-07-04", TYPE_KHAC, "Học Trại Buổi 8"),
    ("2027-07-11", TYPE_THANHLE, "Chúa Nhật 15 Thường Niên Năm B, Chào cờ (VĐ)"),
]

# --- explicit time overrides: (date, name) -> (start, end|None) ------------
# Non-Sunday THANHLE days + OTHER items not covered by the fixed rules below.

TIME_OVERRIDES: dict[tuple[str, str], tuple[str, str | None]] = {
    ("2026-09-24", "Thứ Năm, Lễ Trung Thu (Văn nghệ + Phát quà)"): ("18:00", "19:00"),
    ("2026-09-25", "Thứ Sáu, Đi Lân Quanh Xứ"): ("18:00", None),
    ("2026-12-24", "Thứ Năm, Lễ Canh Thức Giáng Sinh"): ("18:00", "19:30"),
    ("2026-12-25", "Thứ Sáu, Lễ Giáng Sinh"): ("05:00", None),
    ("2027-01-01", "Thứ Sáu, Lễ Mẹ Thiên Chúa"): ("05:00", None),
    ("2027-02-06", "Thứ Bảy, Tết Nguyên Đán Đinh Mùi 2027"): ("05:00", None),
    ("2027-02-10", "Thứ Tư, Lễ Tro"): ("17:30", "18:30"),
    ("2027-03-19", "Thứ Sáu, Lễ Thánh Giuse"): ("17:30", "18:00"),
    ("2027-03-25", "Thứ Năm Tuần Thánh, Lễ Vượt Qua"): ("17:30", "19:00"),
    ("2027-03-26", "Thứ Sáu Tuần Thánh, Tưởng Niệm Cuộc Thương Khó Chúa Giêsu"): (
        "17:00",
        "19:00",
    ),
    ("2027-03-27", "Thứ Bảy Tuần Thánh, Lễ Vọng Phục Sinh"): ("17:30", "19:30"),
    ("2027-06-10", "Thứ Năm, Ban Bí Tích Thêm Sức (Dự kiến)"): ("17:30", "19:30"),
    ("2027-05-07", "Thứ Sáu, GLV Tĩnh Tâm"): ("17:30", "23:50"),
    ("2027-05-08", "Thứ Bảy, GLV Tĩnh Tâm"): ("00:00", "13:30"),
}

# --- http ------------------------------------------------------------------


class Abort(Exception):
    """Stop script with a message."""


def request(
    base_url: str, cookie: str, method: str, path: str, body: dict | None = None
) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        base_url + path,
        data=data,
        method=method,
        headers={
            "Cookie": cookie,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read().decode()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        if exc.code == 401:
            raise Abort(
                "401 Unauthorized — session cookie invalid or expired. "
                "Copy a fresh cookie from logged-in browser."
            ) from exc
        raise Abort(f"{method} {path} failed: HTTP {exc.code}\n{detail}") from exc
    except urllib.error.URLError as exc:
        raise Abort(f"cannot reach {base_url}: {exc.reason}") from exc
    return json.loads(payload) if payload else {}


def normalize_cookie(token: str) -> str:
    token = token.strip()
    if "=" in token:
        return token
    return f"{DEFAULT_COOKIE_NAME}={token}"


# --- time resolution -------------------------------------------------------


def resolve_time(
    date_str: str, activity_type: int, name: str
) -> tuple[str, str | None]:
    override = TIME_OVERRIDES.get((date_str, name))
    if override is not None:
        return override

    date = datetime.strptime(date_str, "%Y-%m-%d")
    if activity_type == TYPE_THANHLE:
        if date.weekday() == 6:
            return SUNDAY_START, SUNDAY_END
        raise Abort(f'THANHLE {date_str} "{name}" has no time override')

    if activity_type == TYPE_GIAOLY:
        return GIAOLY_START, GIAOLY_END

    # TYPE_KHAC (OTHER)
    if name.startswith(FIELD_TRIP_PREFIX):
        return GIAOLY_START, GIAOLY_END
    if name.startswith(CONFESSION_PREFIX):
        return CONFESSION_START, CONFESSION_END
    raise Abort(f'OTHER {date_str} "{name}" has no time override')


def build_payload(date_str: str, activity_type: int, name: str) -> dict:
    start, end = resolve_time(date_str, activity_type, name)
    for value in (start, end):
        if value is not None:
            try:
                datetime.strptime(value, "%H:%M")
            except ValueError as exc:
                raise Abort(f'bad time "{value}" for {date_str} "{name}"') from exc
    return {
        "schedule_activity_type_id": activity_type,
        "name": name,
        "start_at": f"{date_str}T{start}:00",
        "end_at": f"{date_str}T{end}:00" if end else None,
        "is_attendence_check": activity_type != TYPE_KHAC,
    }


def dedup_key(name: str, start_at: str) -> tuple[str, str]:
    parsed = datetime.fromisoformat(start_at.replace("Z", "+00:00"))
    return name, parsed.strftime("%Y-%m-%d %H:%M")


# --- main ------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import lịch sinh hoạt activities")
    parser.add_argument(
        "--token",
        default=os.environ.get("CMS_DASHBOARD_COOKIE"),
        help="session cookie (name=value or bare value), env CMS_DASHBOARD_COOKIE",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="resolve times + print payloads, skip POST",
    )
    args = parser.parse_args()
    if not args.token:
        parser.error("--token required (or set CMS_DASHBOARD_COOKIE)")
    return args


def main() -> int:
    args = parse_args()
    cookie = normalize_cookie(args.token)

    existing_raw = request(args.base_url, cookie, "GET", SCHEDULES_PATH)
    existing = {
        dedup_key(item["name"], item["start_at"])
        for item in existing_raw.get("data", [])
    }

    created = skipped = 0
    try:
        for date_str, activity_type, name in ENTRIES:
            payload = build_payload(date_str, activity_type, name)
            start_at = payload["start_at"]
            if dedup_key(name, start_at) in existing:
                print(f"skip (exists): {date_str} {name}")
                skipped += 1
                continue
            if args.dry_run:
                print(f"DRY: {json.dumps(payload, ensure_ascii=False)}")
                created += 1
                continue
            request(args.base_url, cookie, "POST", SCHEDULES_PATH, payload)
            print(f"created: {date_str} {name}")
            created += 1
    except KeyboardInterrupt:
        print("\ninterrupted")
        return 130

    print(
        f"\ndone: {created} {'would create' if args.dry_run else 'created'}, "
        f"{skipped} skipped"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Abort as exc:
        print(f"ABORT: {exc}", file=sys.stderr)
        sys.exit(1)
