---
title: 修复时间bug
description: An introduction to using the note feature in Astro Cactus
publishDate: "2024-12-13 16:35"
---

  打开文件
  `src/content.config.ts`

  将44行
  `const note = defineCollection()`中的
  ```ts
  .datetime({ offset: true }) // Ensures ISO 8601 format with offsets allowed (e.g. "2024-01-01T00:00:00Z" and "2024-01-01T00:00:00+02:00")
	.transform((val) => new Date(val)),
  ```
  改为：
  ```ts
  .refine((val) => {
				// 修改：解析自定义格式的日期字符串
				const datePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
				return datePattern.test(val);
			}, "Invalid date format. Expected YYYY-MM-DD HH:mm")
			.transform((val) => {
				const [datePart, timePart] = val.split(" ");
				if (!datePart || !timePart) {
					throw new Error("Invalid date format. Expected YYYY-MM-DD HH:mm");
				}
				const [year, month, day] = datePart.split("-");
				const [hour, minute] = timePart.split(":");
				if (!year || !month || !day || !hour || !minute) {
					throw new Error("Invalid date format. Expected YYYY-MM-DD HH:mm");
				}
				return new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute));
			}),
  ```
